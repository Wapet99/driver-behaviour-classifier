# Memory Bank

## Project Brief

Build an edge‑optimised PyTorch driver‑behaviour classifier with a FastAPI inference service deployed on AWS EC2, S3‑hosted model artifacts, CloudWatch logging, and a React dashboard for real‑time predictions. 
This file serves as the persistent context for design decisions, architecture, and development progress.

## Technical Context

- **Core Objective:** Build an end‑to‑end ML system featuring cloud deployment (AWS), edge inference, and a user‑facing interface.
- **Technologies:** PyTorch, ONNX Runtime, FastAPI, React, AWS EC2/S3/CloudWatch, Docker, Nginx.
- **Architecture:**

    - **Model:** Model training pipeline producing PyTorch and ONNX artifacts. Lightweight PyTorch CNN or MobileNetV3 trained to classify driver actions.
    - **Backend:** FastAPI inference server with async endpoints, S3-hosted model weights, CloudWatch logging.
    - **Infra:** Backend deployed as a Docker container on AWS ECS Fargate behind an ALB, with S3‑hosted model artifacts, IAM‑based access, CloudWatch Logs for JSON‑structured application logs, CloudWatch Metrics and Alarms for inference latency and error rates, and IaC (Terraform)
    - **Frontend:** Minimal React dashboard to upload images for real‑time inference.
    - **Edge:** Edge inference module using quantized ONNX model.

- **APIs:** FastAPI /predict endpoint, health checks, S3 artifact retrieval.
- **Constraints:** Lightweight model suitable for edge devices, low‑latency inference, clean separation of backend/frontend/edge components.
- **Training Dataset:** Kaggle State Farm Distracted Driver Detection

### Backend Runtime Conventions
- Backend runs inside Docker with `WORKDIR=/app`.
- Application code is copied into `/app/app`
- Local model path inside container: `/app/app/tmp/model.onnx`.
- Model loading strategy:
- Check local file
- If missing, attempt async S3 download
- Logging uses JSON format for CloudWatch compatibility.
- All API endpoints are async.

### Model Artifacts
- Primary model: `minicnn_int8.onnx` (quantised).
- Input shape: `(1, 3, 224, 224)` (RGB, normalised).
- Preprocessing: resize → center crop → normalise (mean/std).
- Output: logits for 10 driver‑behaviour classes.
- Class mapping stored in `postprocessing.py`.

### Backend Environment Variables
- `ENV` — local | production
- `DEBUG` — enable verbose logging
- `LOG_LEVEL` — INFO/DEBUG
- `MODEL_LOCAL_PATH` — path to ONNX model inside container
- `S3_MODEL_BUCKET` — bucket for model artifacts
- `S3_MODEL_KEY` — key for ONNX model
- `AWS_REGION` — region for S3 access

Local dev uses dummy AWS credentials; EC2 uses IAM role.

## Active Context

- **Current Task:** AWS infra and deployment
- **Recent Changes:**
    - Implemented FastAPI service structure.
    - Implemented preprocessing.py and postprocessing.py
    - Implemented onnx_loader.py and inference.py
    - Fixed issue where inference.py importing session from onnx_loader created a new None variable, instead import onnx_loader and use `session = onnx_loader.session`
    - Updated logging and config to better prepare for AWS deployment.
    - Implemented Dockerfile and requirements.txt, backend can now build and run through docker.
- **Next Steps:**
    - Outline AWS deployment workflow.
    - Begin edge inference design.

### Working directory
```
driver-behaviour-classifier/
│
├── backend/
|   ├── app/
|   │   ├── api/
|   │   │   ├── v1/
|   │   │   │   ├── predict.py
|   │   │   │   └── health.py
|   │   │   └── __init__.py
|   │   │
|   │   ├── core/
|   │   │   ├── config.py
|   │   │   ├── logging.py
|   │   │   └── s3.py
|   │   │
|   │   ├── models/
|   │   │   ├── onnx_loader.py
|   │   │   └── inference.py
|   │   │
|   │   ├── schemas/
|   │   │   ├── predict.py
|   │   │   └── health.py
|   │   │
|   │   ├── utils/
|   │   │   ├── preprocessing.py
|   │   │   └── postprocessing.py
|   │   │
|   │   ├── main.py
|   │   └── __init__.py
|   │
|   ├── tests/
|   │   ├── test_predict.py
|   │   ├── test_health.py
|   │   └── test_inference.py
|   │
|   ├── Dockerfile
|   ├── requirements.txt
|   └── README.md
│
├── frontend/
│   └── README.md
│
├── infra/
│   └── README.md
│
├── model/
│   ├── dataset.py
│   ├── projectmodels.py
│   ├── README.md
│   ├── train.py
│   ├── data/
│   ├── checkpoints/
│   ├── runs/
│   ├── notebooks/
│   |   ├── data_exploration.ipynb
│   |   └── model_comparison.ipynb
│   └── onnx/
│       ├── minicnn.onnx
│       └── minicnn_int8.onnx
│
├── memorybank.md
├── README.md
└── .gitignore
```

## Progress

- **Completed:**

    - Project concept defined.
    - Repository structure drafted.
    - Memory bank initialised.
    - Data exploration notebook created.
    - Dataset class and transforms implemented.
    - Model comparison notebook created.
    - Training script scaffold created.
    - Training script completed
    - Trained 5 models, including 1 custom.
    - Created notebook to export MiniCNN model to ONNX and compare.
    - Created FastAPI backend template
    - Implemented backend pre- and postprocessing
    - Implemented onnx_loader.py and inference.py
    - Fixed issue where inference.py importing session from onnx_loader created a new None variable, instead import onnx_loader and use `session = onnx_loader.session`
    - Updated logging and config to better prepare for AWS deployment.
    - Implemented Dockerfile and requirements.txt, backend can now build and run through docker.

- **Blockers:** None.

- **Evolving Decisions:**

    - Frontend React deployment via S3/CloudFront
    - Containerised backend pushed to ECR
    - ECS Fargate service + ALB defined via Terraform
    - CloudWatch dashboard for inference latency
    - Choice of edge device (Raspberry Pi vs simulated environment).
    - Design of frontend UI
