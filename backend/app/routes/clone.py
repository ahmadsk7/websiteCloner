from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from ..services.scraper import Scraper
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class CloneRequest(BaseModel):
    url: HttpUrl

@router.post("/clone")
async def clone_website(request: CloneRequest):
    try:
        logger.info("=== New Clone Request ===")
        logger.info(f"Request received with URL: {request.url}")
        logger.info(f"Request type: {type(request.url)}")
        
        # Initialize scraper
        logger.info("Initializing scraper...")
        scraper = Scraper()
        
        # Scrape the website
        logger.info("Starting website scraping...")
        design_context = await scraper.scrape(str(request.url))
        
        logger.info("Scraping completed, preparing response...")
        # For now, just return the scraped content
        # In the future, we'll add AI generation here
        response = {
            "html": design_context["html"],
            "design_context": design_context
        }
        logger.info("Sending response back to client...")
        logger.info(f"Response size: {len(str(response))} bytes")
        return response
        
    except Exception as e:
        logger.error("=== Error in Clone Request ===")
        logger.error(f"Error cloning website: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error traceback: {e.__traceback__}")
        raise HTTPException(status_code=500, detail=str(e)) 