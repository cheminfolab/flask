"""
Structured logging without extra dependencies.

- RequestIdMiddleware: takes X-Request-ID from nginx (or generates one),
  returns it in the response and attaches it to every log record of the request.
- JsonFormatter: one JSON object per line on stdout (`docker compose logs`).
"""
import contextvars
import json
import logging
import re
import uuid
from datetime import datetime, timezone

_request_id = contextvars.ContextVar('request_id', default='-')
_VALID_ID = re.compile(r'^[A-Za-z0-9._-]{1,64}$')


def client_ip(request):
    """
    Client address as DRF's throttling sees it: the X-Forwarded-For entry added by
    the trusted proxies (NUM_PROXIES, nginx = 1), never a client-supplied value.
    """
    from django.conf import settings
    meta = request.META
    forwarded = meta.get('HTTP_X_FORWARDED_FOR')
    proxies = settings.REST_FRAMEWORK.get('NUM_PROXIES')
    if forwarded and proxies:
        addresses = [part.strip() for part in forwarded.split(',')]
        return addresses[-min(proxies, len(addresses))]
    return meta.get('REMOTE_ADDR', '-')


class RequestIdMiddleware:
    header = 'HTTP_X_REQUEST_ID'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming = request.META.get(self.header, '')
        # accept only well-formed ids, so clients cannot inject content into logs
        request_id = incoming if _VALID_ID.match(incoming) else uuid.uuid4().hex
        token = _request_id.set(request_id)
        try:
            response = self.get_response(request)
        finally:
            _request_id.reset(token)
        response['X-Request-ID'] = request_id
        return response


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = _request_id.get()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            'time': datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(timespec='milliseconds'),
            'level': record.levelname,
            'logger': record.name,
            'request_id': getattr(record, 'request_id', '-'),
            'message': record.getMessage(),
        }
        for key in ('status_code', 'method', 'path', 'event', 'client_ip'):
            if hasattr(record, key):
                entry[key] = getattr(record, key)
        request = getattr(record, 'request', None)
        if request is not None and hasattr(request, 'method'):
            entry.setdefault('method', request.method)
            entry.setdefault('path', request.path)
        if record.exc_info:
            entry['exception'] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False)
