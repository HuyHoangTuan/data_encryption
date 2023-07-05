from concurrent.futures import ThreadPoolExecutor
from src.configs import MAX_WORKERS
from .get_handlers import *
from .post_handlers import *
worker_manager = ThreadPoolExecutor(max_workers=MAX_WORKERS)


def handle_test_api(**kwargs):
    worker = worker_manager.submit(TestAPI.process, **kwargs)
    return worker.result()


def handle_compress_audio(**kwargs):
    worker = worker_manager.submit(CompressAudio.process, **kwargs)
    return worker.result()