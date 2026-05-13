from pydantic import BaseSettings

class Settings(BaseSettings):
    MODEL_S3_BUCKET: str = "driver-behaviour-models"
    MODEL_S3_KEY: str = "minicnn_int8.onnx"
    MODEL_LOCAL_PATH: str = "/tmp/model.onnx"

settings = Settings()