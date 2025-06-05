from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.clone import router as clone_router

app = FastAPI(title="Website Cloner API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clone_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 