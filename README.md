# Driver Behaviour Classifier with AWS-deployed FastAPI Inference Service

An edge‑optimised PyTorch driver‑behaviour classifier with a FastAPI inference service deployed on AWS ECS, S3‑hosted model artifacts, CloudWatch logging, and a React frontend for real‑time predictions.

## Architecture
- Backend: FastAPI backend with CORS, built to Docker image and uploaded to AWS ECR
- Frontend: Simple React frontend to upload and preview image, request prediction, and view results.
- Infra: Terraform IaC to deploy to AWS
- Model: Notebooks and python training files for training, evaluating, comparing, exporting, and quantising models.
    - Final model was a tiny custom CNN exported to ONNX and quantised to int8, edge-deployment ready.

### Tree
```bash
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
|   ├── index.html
|   ├── package.json
|   ├── tsconfig.json
|   ├── vite.config.ts
|   ├── README.md
│   └── src/
|       ├── App.tsx
|       ├── index.css
│       └── main.tsx
|
├── infra/
|   ├── main.tf
|   ├── variables.tf
|   ├── outputs.tf
|   ├── README.md
|   │
|   ├── modules/
|   │   ├── network/
|   │   │   ├── main.tf
|   │   │   ├── variables.tf
|   │   │   └── outputs.tf
|   │   ├── ecr/
|   │   │   ├── main.tf
|   │   │   ├── variables.tf
|   │   │   └── outputs.tf
|   │   ├── ecs/
|   │   │   ├── main.tf
|   │   │   ├── variables.tf
|   │   │   └── outputs.tf
|   │   ├── alb/
|   │   │   ├── main.tf
|   │   │   ├── variables.tf
|   │   │   └── outputs.tf
|   │   ├── cloudwatch/
|   │   │   ├── main.tf
|   │   │   ├── variables.tf
|   │   │   └── outputs.tf
|   │   └── iam/
|   │       ├── main.tf
|   │       ├── variables.tf
|   │       └── outputs.tf
|   │
|   └── envs/
|       ├── dev/
|       │   └── terraform.tfvars
|       └── prod/
|           └── terraform.tfvars
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

## Tech Stack
PyTorch, FastAPI, React, AWS ECS/ECR/ALB/S3/CloudWatch, ONNX Runtime

## Notes
- Can't get certificates for HTTPS for ALB domain, so backend only supports http, meaning frontend needs to be hosted on http to get predictions.
- While the quantised model is fast and tiny to be ready for edge-deployment, this project targetted cloud deployment instead, hence the Docker image and AWS hosting. The model is small enough that the more logical method of hosting would be to eliminate the cloud backend entirely and run the model from the browser using WASM or WebGPU. This would have the extra privacy benefit of data never leaving the user device.