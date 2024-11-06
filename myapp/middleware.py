# app/middleware.py
from .context import get_current_sync_source
import threading


class SyncContextMiddleware:
    """
    Middleware to set sync_source from request headers or parameters.
    """

    _thread_locals = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._thread_locals.sync_source = "odoo"
        response = self.get_response(request)
        self._thread_locals.sync_source = None
        return response
