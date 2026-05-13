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
    - **Infra:** AWS EC2 deployment using systemd or Docker + Nginx reverse proxy.
    - **Frontend:** Minimal React dashboard to upload images for real‑time inference.
    - **Edge:** Edge inference module using quantized ONNX model.

- **APIs:** FastAPI /predict endpoint, health checks, S3 artifact retrieval.
- **Constraints:** Lightweight model suitable for edge devices, low‑latency inference, clean separation of backend/frontend/edge components.
- **Training Dataset:** Kaggle State Farm Distracted Driver Detection

## Active Context

- **Current Task:** Implement FastAPI backend core services (core, utils, models)
- **Recent Changes:**
    - Implemented FastAPI service structure.
    - Implemented preprocessing.py and postprocessing.py
    - Implemented onnx_loader.py and inference.py
    - Fixed issue where inference.py importing session from onnx_loader created a new None variable, instead import onnx_loader and use `session = onnx_loader.session`
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

- **Blockers:** None.

- **Evolving Decisions:**

    - Choice of edge device (Raspberry Pi vs simulated environment).
    - Deployment strategy (Docker vs systemd).
    - ONNX quantization approach (dynamic vs QAT).
