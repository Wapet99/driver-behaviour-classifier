import onnxruntime as ort
from fastapi import HTTPException, status
from app.core.config import settings
import os

# Global ONNXRuntime session
session = None

def _create_session(model_path: str):
    """
    Internal helper to create the ONNXRuntime session with safe defaults.
    """
    try:
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        # CPU execution provider
        providers = ["CPUExecutionProvider"]

        return ort.InferenceSession(
            model_path,
            sess_options=sess_options,
            providers=providers
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load ONNX model: {str(e)}"
        )

async def load_model():
    """
    Loads the ONNX model into a global session.
    Called once during FastAPI lifespan startup.
    """
    global session

    model_path = settings.MODEL_LOCAL_PATH

    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model file not found at {model_path}"
        )
    
    session = _create_session(model_path)
    return session