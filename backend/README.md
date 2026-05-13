


## Architecture
```
backend/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── predict.py
│   │   │   └── health.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── s3.py
│   │
│   ├── models/
│   │   ├── onnx_loader.py
│   │   └── inference.py
│   │
│   ├── schemas/
│   │   ├── predict.py
│   │   └── health.py
│   │
│   ├── utils/
│   │   ├── preprocessing.py
│   │   └── postprocessing.py
│   │
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   ├── test_predict.py
│   ├── test_health.py
│   └── test_inference.py
│
├── Dockerfile
├── requirements.txt
└── README.md
```

## Running locally with docker
Ensure model.onnx exists at backend/app/tmp/model.onnx and .env exists at backend/.env
From backend/ run:
```bash
docker build -t driver-backend .
docker run --env-file .env -p 8000:8000 driver-backend
```

### .env format
```
# --- APP ---
ENV=local
DEBUG=True
LOG_LEVEL=INFO

# --- MODEL ---
MODEL_LOCAL_PATH=/app/app/tmp/model.onnx
S3_MODEL_BUCKET=driver-behaviour-classifier
S3_MODEL_KEY=models/minicnn.onnx

# --- AWS ---
AWS_REGION=ap-southeast-2
AWS_ACCESS_KEY_ID=local-dev-only
AWS_SECRET_ACCESS_KEY=local-dev-only
```