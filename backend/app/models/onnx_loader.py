import onnxruntime as ort
from app.core.config import settings

session = None

async def load_model():
    global session
    session = ort.InferenceSession(settings.MODEL_LOCAL_PATH)