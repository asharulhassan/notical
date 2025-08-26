import os
import logging
from rq import Queue, Worker, Connection
from redis import Redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis connection
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = Redis.from_url(redis_url)

# Create a queue for background jobs
task_queue = Queue("swerve_tasks", connection=redis_conn)

def start_worker():
    """
    Starts an RQ worker that listens to the 'swerve_tasks' queue.
    """
    logger.info("Starting worker for queue: swerve_tasks")
    with Connection(redis_conn):
        worker = Worker([task_queue])
        worker.work()


# Example background task
def background_task(name: str):
    """
    Example async task to verify worker setup.
    """
    logger.info(f"Running background task for {name}")
    return f"Hello, {name}! Background task executed successfully."
