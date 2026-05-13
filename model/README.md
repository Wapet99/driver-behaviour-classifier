# model/ — Model Training, Export, and Edge‑Optimisation
The model module contains all training, evaluation, and export logic for the driver‑behaviour classifier.
It produces both **PyTorch** and **ONNX** artifacts, including an **int8‑quantised** version optimised for edge inference.
This directory is the foundation of the ML pipeline powering the FastAPI backend and the edge runtime.

## Overview
The goal of this component is to train a **lightweight CNN‑based classifier** capable of recognising distracted‑driving behaviours from the *State Farm Distracted Driver Detection* dataset. The resulting model must be:

- **Small enough** for edge devices
- **Fast enough** for real‑time inference
- **Portable** across PyTorch, ONNX, and quantised runtimes
- **Cloud‑deployable** via S3‑hosted artifacts

The training pipeline outputs:

- A **PyTorch checkpoint** (`{model_name}.pth`)

The 

- A **standard ONNX model** (`minicnn.onnx`)
- An **int8‑quantised ONNX model** (`minicnn_int8.onnx`) for edge devices

Explore the architecture in more detail via `projectmodels.py`, or review the training logic in `train.py`.

## Directory Structure
- **dataset.py** - Dataset + transforms for State Farm dataset
- **projectmodels.py** - MiniCNN + other model definitions
- **train.py** - Full training loop, logging, checkpointing
- **data/** - Local dataset storage (ignored in Git)
- **checkpoints/** - Saved PyTorch weights
- **runs/** - TensorBoard logs
- **notebooks/**
    - `data_exploration.ipynb`
    - `model_comparison.ipynb`
    - `onnx_export_and_quant.ipynb` (exports & quantises MiniCNN)
- **onnx/**
    - `minicnn.onnx`
    - `minicnn_int8.onnx`

## Model Architecture
The current best‑performing model is **MiniCNN**, a custom compact convolutional network designed for:

- Low parameter count
- Fast inference on CPU‑only environments
- Compatibility with ONNX Runtime
- Straightforward quantisation

Alternative architectures (e.g., MobileNetV3‑Small, ResNet18, ShuffleNetV2, EfficientNet-B0) were evaluated in model_comparison.ipynb, but MiniCNN offered the best trade‑off between accuracy and edge performance.

## Training Pipeline
Training is orchestrated through `train.py` and includes:

- Dataset loading + augmentation
- Configurable hyperparameters
- Checkpoint saving
- TensorBoard logging
- Validation loop with accuracy + loss metrics

The dataset is sourced from the **State Farm Distracted Driver Detection** Kaggle competition and preprocessed into a standard image‑classification format.

## ONNX Export & Quantisation
The notebook `onnx_export_and_quant.ipynb` performs:

1. **PyTorch -> ONNX export**
2. **Dynamic quantisation to int8**
3. **Model validation using ONNX Runtime**
4. **Performance comparison (latency + size)**

Artifacts are saved to:

```
model/onnx/
├── minicnn.onnx
└── minicnn_int8.onnx
```
These models are consumed by:

- The FastAPI backend (standard ONNX)
- The edge inference module (int8 ONNX)

Explore the quantisation workflow in onnx_export_and_quant.ipynb.