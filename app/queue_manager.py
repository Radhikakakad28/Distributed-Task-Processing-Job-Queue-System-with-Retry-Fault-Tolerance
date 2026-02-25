import json
import time
from app.redis_client import redis_client

QUEUE_KEY = "job_queue"
STATUS_KEY = "job_status"
DEAD_LETTER_KEY = "dead_letter_queue"


def enqueue_job(job, delay=0):
    """
    Add job to queue with optional delay.
    Uses timestamp as score for scheduling.
    """
    score = time.time() + delay
    redis_client.zadd(
        QUEUE_KEY,
        {json.dumps(job): score}
    )
    redis_client.hset(STATUS_KEY, job["task_id"], "queued")


def update_status(task_id, status):
    redis_client.hset(STATUS_KEY, task_id, status)


def get_status(task_id):
    return redis_client.hget(STATUS_KEY, task_id)


def dequeue_job():
    """
    Fetch job whose scheduled time <= current time
    """
    now = time.time()

    jobs = redis_client.zrangebyscore(
        QUEUE_KEY,
        0,
        now,
        start=0,
        num=1
    )

    if not jobs:
        return None

    job = jobs[0]

    # atomic remove
    redis_client.zrem(QUEUE_KEY, job)

    return json.loads(job)


def move_to_dead_letter(job):
    redis_client.rpush(DEAD_LETTER_KEY, json.dumps(job))
    redis_client.hset(STATUS_KEY, job["task_id"], "failed")