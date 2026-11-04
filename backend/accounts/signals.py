import logging

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from api.log import client_ip

security_log = logging.getLogger('flask.security')


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request=None, **kwargs):
    # No email or password in the log: only the event and the client address,
    # enough to spot brute-force attempts (throttling blocks them, see settings).
    address = client_ip(request) if request is not None else '-'
    security_log.warning('login failed', extra={'event': 'login_failed', 'client_ip': address})
