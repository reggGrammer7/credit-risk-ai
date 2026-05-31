from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    model_ready = Path("models/credit_model.pkl").exists()
    return {
        "status": "ok",
        "model_loaded": model_ready,
    }
