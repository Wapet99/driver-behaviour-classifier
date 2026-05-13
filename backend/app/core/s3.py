import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
from app.core.logging import get_logger
from pathlib import Path

logger = get_logger(__name__)

async def download_model_from_s3():
    local_path = Path(settings.MODEL_LOCAL_PATH)
    if local_path.exists():
        logger.info(f"Model already present at {local_path}")
        return local_path
    
    logger.info(
        f"Downloading model from s3://{settings.MODEL_S3_BUCKET}/{settings.MODEL_S3_KEY} to {local_path}"
    )

    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client("s3") #, region_name=settings.AWS_REGION
    try:
        s3.download_file(
            settings.MODEL_S3_BUCKET,
            settings.MODEL_S3_KEY,
            str(local_path),
        )
    except ClientError as e:
        logger.error(f"Failed to download model from S3: {e}")
        raise

    logger.info("Model download complete")
    return local_path