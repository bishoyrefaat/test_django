# app/context.py
import threading

_thread_locals = threading.local()


class SyncSourceContext:
    """
    Context manager to set sync_source in thread-local storage.
    """

    def __init__(self, source):
        self.source = source

    def __enter__(self):
        _thread_locals.sync_source = self.source

    def __exit__(self, exc_type, exc_val, exc_tb):
        _thread_locals.sync_source = None


def get_current_sync_source():
    return getattr(_thread_locals, "sync_source", None)
