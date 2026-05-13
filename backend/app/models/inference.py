from app.models.onnx_loader import session
from app.utils.preprocessing import preprocess_image
from app.utils.postprocessing import postprocess_output
from app.schemas.predict import PredictionResponse

async def run_inference(file):
    image = await preprocess_image(file)
    outputs = session.run(None, {"input": image})
    prediction = postprocess_output(outputs)
    return PredictionResponse(**prediction)