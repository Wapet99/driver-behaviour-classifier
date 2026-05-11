# Memory Bank

## Project Brief

Build an edge‑optimised PyTorch driver‑behaviour classifier with a FastAPI inference service deployed on AWS EC2, S3‑hosted model artifacts, CloudWatch logging, and a React dashboard for real‑time predictions. 
This file serves as the persistent context for design decisions, architecture, and development progress.

## Technical Context

- **Core Objective:** Build an end‑to‑end ML system featuring cloud deployment (AWS), edge inference, and a user‑facing interface.
- **Technologies:** PyTorch, ONNX Runtime, FastAPI, React, AWS EC2/S3/CloudWatch, Docker, Nginx.
- **Architecture:**

    - **Model:** Model training pipeline producing PyTorch and ONNX artifacts. Lightweight PyTorch CNN or MobileNetV3 trained to classify driver actions.
    - **Backend:** FastAPI inference server with async endpoints, model pulled from S3, structured logging to CloudWatch.
    - **Infra:** AWS EC2 deployment using systemd or Docker + Nginx reverse proxy.
    - **Frontend:** Minimal React dashboard to upload images for real‑time inference.
    - **Edge:** Edge inference module using quantized ONNX model.

- **APIs:** FastAPI /predict endpoint, health checks, S3 artifact retrieval.
- **Constraints:** Lightweight model suitable for edge devices, low‑latency inference, clean separation of backend/frontend/edge components.
- **Training Dataset:** Kaggle State Farm Distracted Driver Detection

## Active Context

- **Current Task:** Preparing exploration notebooks.
- **Recent Changes:** Initial creation of project brief, technical context, and structure.
- **Next Steps:**

    - Define model training pipeline.
        - Exploration notebooks
        - Processing, training, and util files
    - Draft FastAPI service structure.
    - Outline AWS deployment workflow.
    - Begin edge inference design.

## Progress

- **Completed:**

    - Project concept defined.
    - Repository structure drafted.
    - Memory bank initialised.

- **Blockers:** None at this stage.

- **Evolving Decisions:**

    - Model selection for driver behavior classification.
    - Choice of edge device (Raspberry Pi vs simulated environment).
    - Deployment strategy (Docker vs systemd).
