import logging
from typing import Dict, Any
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self):
        self.timeout = 30000  # 30 seconds timeout for browser operations
        
    async def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape a website using Playwright to handle modern websites and JavaScript.
        """
        logger.info(f"Starting scrape of {url}")
        browser = None
        
        try:
            logger.info("Initializing Playwright...")
            async with async_playwright() as p:
                # Launch browser
                logger.info("Launching browser...")
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                logger.info("Creating browser context...")
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                
                # Create new page
                logger.info("Creating new page...")
                page = await context.new_page()
                
                # Set timeout
                page.set_default_timeout(self.timeout)
                
                # Navigate to URL
                logger.info(f"Navigating to {url}")
                try:
                    response = await page.goto(url, wait_until='networkidle', timeout=self.timeout)
                    if not response:
                        raise Exception("Failed to load page - no response received")
                    logger.info(f"Page loaded with status: {response.status}")
                except PlaywrightTimeoutError as e:
                    logger.error(f"Timeout while loading page: {str(e)}")
                    raise Exception(f"Timeout while loading page: {str(e)}")
                
                logger.info("Page loaded, waiting for content...")
                # Wait for content to load
                await page.wait_for_load_state('domcontentloaded')
                
                # Get the page content
                logger.info("Getting page content...")
                content = await page.content()
                
                # Parse with BeautifulSoup
                logger.info("Parsing HTML...")
                soup = BeautifulSoup(content, 'html.parser')
                
                # Inline external CSS
                def inline_css(soup, base_url):
                    for link in soup.find_all('link', rel='stylesheet'):
                        href = link.get('href')
                        if href:
                            css_url = href if href.startswith('http') else urljoin(base_url, href)
                            try:
                                css_content = requests.get(css_url, timeout=5).text
                                style_tag = soup.new_tag('style')
                                style_tag.string = css_content
                                link.replace_with(style_tag)
                            except Exception as e:
                                logger.error(f"Failed to fetch CSS from {css_url}: {e}")
                    return soup

                soup = inline_css(soup, url)
                content = str(soup)
                
                # Extract basic information
                title = soup.title.string if soup.title else ''
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                description = meta_desc['content'] if meta_desc else ''
                
                logger.info("Extracting styles...")
                # Get computed styles
                styles = await page.evaluate("""() => {
                    const styles = {};
                    const elements = document.querySelectorAll('*');
                    elements.forEach(el => {
                        const computedStyle = window.getComputedStyle(el);
                        const color = computedStyle.color;
                        const bgColor = computedStyle.backgroundColor;
                        const fontSize = computedStyle.fontSize;
                        if (color !== 'rgb(0, 0, 0)' || bgColor !== 'rgba(0, 0, 0, 0)') {
                            styles[el.tagName.toLowerCase()] = {
                                color,
                                backgroundColor: bgColor,
                                fontSize
                            };
                        }
                    });
                    return styles;
                }""")
                
                logger.info("Extracting images...")
                # Get all images
                images = await page.evaluate("""() => {
                    return Array.from(document.images).map(img => ({
                        src: img.src,
                        alt: img.alt,
                        width: img.width,
                        height: img.height
                    }));
                }""")
                
                # Close browser
                logger.info("Closing browser...")
                await browser.close()
                
                # Prepare response
                result = {
                    'url': url,
                    'html': content,
                    'title': title,
                    'meta': {
                        'description': description
                    },
                    'styles': styles,
                    'assets': {
                        'images': images
                    }
                }
                
                logger.info(f"Successfully scraped {url}")
                return result
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            if browser:
                try:
                    await browser.close()
                except:
                    pass
            raise Exception(f"Failed to scrape website: {str(e)}") 