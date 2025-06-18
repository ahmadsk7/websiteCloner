import logging
from typing import Dict, Any
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import requests
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self):
        self.timeout = 30000  # 30 seconds timeout for browser operations
        
    async def extract_comprehensive_background(self, page, base_url):
        selectors = [
            "body", "html", "main", "#__next", "#root", ".main-wrapper", ".container", "div"
        ]
        backgrounds = []
        for selector in selectors:
            bg = await page.evaluate(f'''
            () => {{
                const el = document.querySelector("{selector}");
                if (!el) return null;
                const style = window.getComputedStyle(el);
                const bg = style.background;
                const bgImg = style.backgroundImage;
                if (bg && bg !== 'none' && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent')
                    return {{selector: "{selector}", style: `background: ${{bg}} !important;`}};
                if (bgImg && bgImg !== 'none')
                    return {{selector: "{selector}", style: `background-image: ${{bgImg}} !important;`}};
                return null;
            }}
            ''')
            if bg:
                backgrounds.append(bg)
        return backgrounds

    def fix_css_urls(self, css, base_url):
        def replacer(match):
            orig_url = match.group(1).strip(' "\'')
            if orig_url.startswith(('http://', 'https://', 'data:')):
                return f"url({orig_url})"
            return f"url({urljoin(base_url, orig_url)})"
        return re.sub(r'url\(([^)]+)\)', replacer, css)

    def debug_css_urls(self, css, base_url):
        urls = re.findall(r'url\([^)]+\)', css)
        logger.info(f"Found CSS URLs: {urls}")
        return self.fix_css_urls(css, base_url)

    def apply_backgrounds_to_soup(self, soup, backgrounds):
        for bg in backgrounds:
            selector = bg['selector']
            style = bg['style']
            el = soup.select_one(selector)
            if el:
                old_style = el.get('style', '')
                if old_style and not old_style.strip().endswith(';'):
                    old_style += ';'
                el['style'] = old_style + style
        return soup

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
                
                # Inline external CSS (with url fix)
                def inline_css(soup, base_url):
                    for link in soup.find_all('link', rel='stylesheet'):
                        href = link.get('href')
                        if href:
                            css_url = href if href.startswith('http') else urljoin(base_url, href)
                            try:
                                css_content = requests.get(css_url, timeout=5).text
                                css_content = self.debug_css_urls(css_content, base_url)
                                style_tag = soup.new_tag('style')
                                style_tag.string = css_content
                                link.replace_with(style_tag)
                            except Exception as e:
                                logger.error(f"Failed to fetch CSS from {css_url}: {e}")
                    return soup

                # Fix image src attributes to be absolute URLs
                def fix_image_srcs(soup, base_url):
                    for img in soup.find_all('img'):
                        src = img.get('src')
                        if src and not src.startswith(('http://', 'https://', 'data:')):
                            img['src'] = urljoin(base_url, src)
                    return soup

                soup = inline_css(soup, url)
                soup = fix_image_srcs(soup, url)

                backgrounds = await self.extract_comprehensive_background(page, url)
                logger.info(f"Detected backgrounds: {backgrounds}")
                # Fix url(...) in background styles
                for bg in backgrounds:
                    bg['style'] = self.fix_css_urls(bg['style'], url)
                soup = self.apply_backgrounds_to_soup(soup, backgrounds)
                content = str(soup)
                
                # Pick the most relevant background style for the frontend
                background_style = ''
                for bg in backgrounds:
                    if bg['selector'] == 'body':
                        background_style = bg['style']
                        break
                if not background_style and backgrounds:
                    background_style = backgrounds[0]['style']
                
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
                    'styles': {**styles, 'background': background_style},
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