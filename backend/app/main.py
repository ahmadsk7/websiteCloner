from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.clone import router as clone_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow GET, POST, and OPTIONS
    allow_headers=["*"],
)

# Include routers
app.include_router(clone_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 