from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from .routes.api import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FloorPlan2D Backend is running"}