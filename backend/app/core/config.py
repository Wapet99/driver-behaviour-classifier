from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    # Runtime
    ENV: str = "local"
    DEBUG: bool = True

    # Model
    MODEL_LOCAL_PATH: str = str(Path(__file__).resolve().parent.parent / "tmp" / "model.onnx")

    # S3
    MODEL_S3_BUCKET: str = "driver-behaviour-classifier"
    MODEL_S3_KEY: str = "models/minicnn_int8.onnx"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_CLOUDWATCH: bool = False
    CLOUDWATCH_LOG_GROUP: str = "driver-behaviour-classifier"
    CLOUDWATCH_LOG_STREAM: str = "backend"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()