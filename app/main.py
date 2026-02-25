from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import threading

from app.producer import create_job
from app.worker import start_workers
from app.queue_manager import get_status


# -----------------------------
# Request Model (Better than dict)
# -----------------------------
class JobRequest(BaseModel):
    payload: dict
    priority: int = 1
    retries: int = 3
    delay: int = 0


# -----------------------------
# Lifespan (Worker Startup)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_thread = threading.Thread(
        target=start_workers,
        daemon=True
    )
    worker_thread.start()
    yield


app = FastAPI(lifespan=lifespan)


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "service": "Distributed Job Queue System"
    }


# -----------------------------
# Submit Job
# -----------------------------
@app.post("/submit")
def submit_job(request: JobRequest):
    job = create_job(
        payload=request.payload,
        priority=request.priority,
        retries=request.retries,
        delay=request.delay
    )

    return {
        "message": "Job submitted successfully",
        "job_id": job["task_id"]
    }


# -----------------------------
# Check Job Status
# -----------------------------
@app.get("/status/{task_id}")
def check_status(task_id: str):
    status = get_status(task_id)

    if not status:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "task_id": task_id,
        "status": status
    }