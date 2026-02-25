import uuid
from typing import Dict, Any
from app.queue_manager import enqueue_job


def create_job(
    payload: Dict[str, Any],
    priority: int = 1,
    retries: int = 3,
    delay: int = 0
):
    """
    Create and enqueue a new job
    """

    job = {
        "task_id": str(uuid.uuid4()),
        "payload": payload,
        "priority": priority,
        "retries": retries
    }

    enqueue_job(job, delay=delay)

    return job