import numpy as np
from fastapi import HTTPException, status

CLASS_NAMES = [
    "safe_driving",
    "texting_right",
    "talking_phone_right",
    "texting_left",
    "talking_phone_left",
    "operating_radio",
    "drinking",
    "reaching_behind",
    "hair_makeup",
    "talking_to_passenger"
]

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=1, keepdims=True)

def postprocess_output(outputs):
    """
    Convert ONNX model outputs into a structured prediction:
    - Apply softmax
    - Extract top-1 class
    - Map index to label
    - Return confidence score
    """

    try:
        logits = outputs[0]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model output format is invalid"
        )
    
    # Softmax
    probs = softmax(logits)

    #Top-1
    top_idx = int(np.argmax(probs, axis=1)[0])
    confidence = float(probs[0][top_idx])

    # Map index to class label
    try:
        label = CLASS_NAMES[top_idx]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model predicted invalid class index: {top_idx}"
        )

    return {"label": label, "confidence": confidence}