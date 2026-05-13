


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