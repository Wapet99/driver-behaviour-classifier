from fastapi import APIRouter, UploadFile, File
from app.schemas.predict import PredictionResponse
from app.models.inference import run_inference

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    result = await run_inference(file)
    return result