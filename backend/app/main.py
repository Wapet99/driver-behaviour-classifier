from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.predict import router as predict_router
from app.api.v1.health import router as health_router
from app.core.logging import configure_logging, get_logger
from app.models.onnx_loader import load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger = get_logger(__name__)
    logger.info("FastAPI app starting")
    await load_model()
    yield

app = FastAPI(
    title="Driver Behaviour Classifier API",
    version="1.0.0",
    lifespan=lifespan,
    )

app.include_router(health_router, prefix="/api/v1")
app.include_router(predict_router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)