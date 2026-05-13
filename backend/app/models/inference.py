from fastapi import HTTPException, status
import app.models.onnx_loader as onnx_loader
from app.utils.preprocessing import preprocess_image
from app.utils.postprocessing import postprocess_output
from app.schemas.predict import PredictionResponse
from app.core.logging import get_logger

logger = get_logger(__name__)

async def run_inference(upload_file):
    """
    Full inference pipeline:
    - Preprocess uploaded image
    - Run ONNX model
    - Postprocess outputs
    - Return PredictionResponse
    """
    session = onnx_loader.session
    # print("ONNX loader module id:", id(session))
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model session is not initialised"
        )

    # Preprocess image to numpy tensor
    image = await preprocess_image(upload_file)
    logger.debug("Preprocessing complete")

    try:
        # ONNXRuntime inference
        outputs = session.run(None, {"input": image})
        logger.debug("Inference completed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model inference failed: {str(e)}"
        )
    
    # Convert raw outputs to label and confidence
    prediction = postprocess_output(outputs)

    return PredictionResponse(**prediction)