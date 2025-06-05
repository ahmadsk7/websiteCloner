from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CloneRequest(BaseModel):
    url: str

@router.post("/clone")
def clone_website(request: CloneRequest):
    # Dummy implementation
    return {"html": f"<h1>Cloned HTML for {request.url}</h1>"} 