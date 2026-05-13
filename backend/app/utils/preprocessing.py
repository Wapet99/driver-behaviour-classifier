import numpy as np
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from fastapi import HTTPException, status

# Model input size
IMG_SIZE = 224

# ImageNet mean/std for normalisation
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

async def preprocess_image(upload_file):
    """
    Convert uploaded image into a NumPy tensor suitable for ONNXRuntime.
    Steps:
    - Read file bytes
    - Decode into PIL image
    - Convert to RGB
    - Resize to model input size
    - Convert to F32
    - Normalise
    - Convert to CHW format
    - Add batch dimension
    """
    # Read bytes and decode
    try:
        contents = await upload_file.read()
        image = Image.open(BytesIO(contents))
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid image"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process uploaded image"
        )

    # RGB
    image = image.convert("RGB")

    # Resize
    image = image.resize((IMG_SIZE, IMG_SIZE))

    # Convert F32
    image_np = np.array(image).astype(np.float32) / 255.0 #might need to be int8 for quantised onnx

    # Normalise
    image_np = (image_np - MEAN) / STD

    # HWC -> CHW
    image_np = np.transpose(image_np, (2, 0, 1))

    # Add batch dim
    image_np = np.expand_dims(image_np, axis=0)

    return image_np
