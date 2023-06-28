from concurrent.futures import ThreadPoolExecutor
from src.configs import MAX_WORKERS
from .get_handlers import TestAPI

worker_manager = ThreadPoolExecutor(max_workers=MAX_WORKERS)


def handle_test_api(**kwargs):
    worker = worker_manager.submit(TestAPI.process, **kwargs)
    return worker.result()
