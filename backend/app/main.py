from fastapi import FastAPI
from app.api.v1.predict import router as predict_router
from app.api.v1.health import router as health_router
from app.core.logging import setup_logging
from app.models.onnx_loader import load_model

app = FastAPI(title="Driver Behaviour Classifier API")

@app.on_event("startup")
async def startup_event():
    setup_logging()
    await load_model()

app.include_router(health_router, prefix="/api/v1")
app.include_router(predict_router, prefix="/api/v1")
