import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import predict, chat, health

app = FastAPI(
    title="Credit Risk AI API",
    description="ML-powered credit risk prediction with LLM explanations",
    version="1.0.0",
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
app.include_router(chat.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Credit Risk AI API", "docs": "/docs"}
