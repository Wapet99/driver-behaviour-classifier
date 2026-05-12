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

- **Current Task:** Implement ONNX export and quantisation notebook.
- **Recent Changes:**
    - Implemented train.py as key model training script
    - Implemented projectmodels.py to house different final models
    - Created custom MiniCNN model with depthwise separable convolutions.
    - Updated model_comparison.ipynb to use well trained models for evaluation.
- **Next Steps:**
    - Draft FastAPI service structure.
    - Outline AWS deployment workflow.
    - Begin edge inference design.

### Working directory
```
driver-behaviour-classifier/
│
├── backend/
│   └── README.md
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
│   └── notebooks/
│       ├── data_exploration.ipynb
│       └── model_comparison.ipynb
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

- **Blockers:** None.

- **Evolving Decisions:**

    - Model selection for driver behavior classification.
    - Choice of edge device (Raspberry Pi vs simulated environment).
    - Deployment strategy (Docker vs systemd).
    - ONNX quantization approach (dynamic vs QAT).
