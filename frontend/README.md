# React + TypeScript + Vite

## Functional and UX requirements
Core features
- Image upload:
    - Select image from disk (JPEG/PNG).
    - Show thumbnail preview and basic metadata (size, dimensions if available).

- Prediction request:
    - Send image to /predict (likely as multipart/form-data unless backend expects base64/JSON).
    - Display:
        - Top predicted class (driver behaviour).
        - Confidence/probability.
        - Full class distribution (optional chart).

Nice-to-have
- Class legend: Human-readable descriptions for the 10 classes (mirroring postprocessing.py mapping).
- Dark/light theme toggle.
- Health indicator:
    - Ping /health on load and periodically (e.g. every 30–60s).
    - Show status badge: “Healthy / Degraded / Down”.

- Inference telemetry (from frontend perspective):
    - Show request latency (ms).
    - Show last error message if a call fails.
    - Maintain a short history of recent predictions (time, class, confidence, latency).

## Frontend architecture and component structure
Tech stack
- React (functional components, hooks).
- TypeScript (strongly recommended for API types).
- Build tool: Vite (for speed)

```
frontend/
  src/
    api/
    index.css
    main.tsx
    App.tsx
```
