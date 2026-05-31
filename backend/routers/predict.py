from fastapi import APIRouter, HTTPException
from schemas.schemas import ApplicantFeatures, PredictionResponse
from services import model_service

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post("", response_model=PredictionResponse)
def predict(applicant: ApplicantFeatures):
    try:
        return model_service.predict(applicant)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
