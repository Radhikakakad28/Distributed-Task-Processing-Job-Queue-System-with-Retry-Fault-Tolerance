import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor

from app.queue_manager import (
    dequeue_job,
    enqueue_job,
    move_to_dead_letter,
    update_status
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_task(job):
    """
    Simulated task processing
    """
    logger.info(f"Processing job {job['task_id']}")
    update_status(job["task_id"], "processing")

    # Simulate random failure
    if random.random() < 0.3:
        raise Exception("Random failure")

    update_status(job["task_id"], "completed")
    logger.info(f"Completed job {job['task_id']}")


def worker_loop():
    while True:
        job = dequeue_job()

        if job:
            try:
                process_task(job)

            except Exception as e:
                logger.error(f"Job {job['task_id']} failed: {str(e)}")

                job["retries"] -= 1

                if job["retries"] > 0:
                    update_status(job["task_id"], "retrying")

                    # Exponential backoff delay
                    delay = 2 ** (3 - job["retries"])
                    enqueue_job(job, delay=delay)

                else:
                    move_to_dead_letter(job)
                    logger.error(
                        f"Job {job['task_id']} moved to Dead Letter Queue"
                    )

        time.sleep(1)


def start_workers(num_workers=3):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for _ in range(num_workers):
            executor.submit(worker_loop)