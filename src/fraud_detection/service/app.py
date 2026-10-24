import time
import uuid
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, create_model
from starlette.background import BackgroundTask

from fraud_detection import db
from fraud_detection.config import settings

_FeaturesBase = create_model(
    "Features",
    __config__={"extra": "forbid"},
    **{name: (float, ...) for name in settings.FEATURE_LIST},
)


class Features(_FeaturesBase):
    pass


class Prediction(BaseModel):
    model_config = {"protected_namespaces": ()}

    score: float
    fraud: bool
    model_version: str
    request_id: str
    latency_ms: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    bundle = joblib.load(settings.model_path)
    app.state.pipeline = bundle["model"]
    app.state.version = bundle["version"]

    app.state.meta = {
        "features": bundle["selected_features"],
        "threshold": bundle["threshold"],
    }
    db.init()
    yield
    app.state.pipeline = None


app = FastAPI(title="fraud-detection-service", version="1.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "model_version": getattr(app.state, "version", "unknown"),
            "fraud_threshold": settings.fraud_threshold}

@app.get("/ready")
def ready():
    if getattr(app.state, "pipeline", None) is  None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {"status": "ready"}



@app.post("/v1/predict")
def predict(x: Features, bg: BackgroundTasks) -> Prediction:
    t0 = time.perf_counter()
    request_id = str(uuid.uuid4())

    payload = x.model_dump()  # x.dict() in pydantic v1
    frame = pd.DataFrame([payload]).reindex(columns=app.state.meta["features"])
    score = float(app.state.pipeline.predict_proba(frame)[0, 1])

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    bg.add_task(db.save_prediction, request_id, payload, score, app.state.version, latency_ms, 200)

    fraud = score >= app.state.meta["threshold"]

    return Prediction(score=score, fraud=fraud, model_version = app.state.version,
                    request_id=request_id, latency_ms=latency_ms)

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    request_id = str(uuid.uuid4())
    errors = jsonable_encoder(exc.errors())
    task = BackgroundTask(
        db.save_prediction, request_id, jsonable_encoder(exc.body), None,
        getattr(app.state, "version", None), 0.0, 422,
    )

    return JSONResponse(
        status_code=422,
        content={"detail": errors, "request_id": request_id},
        background=task,
    )
