from django.db.models import ProtectedError, RestrictedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler, set_rollback


def exception_handler(exc, context):
    """
    DRF's handler, plus 409 Conflict for deletes blocked by on_delete=PROTECT /
    RESTRICT instead of an unhandled 500.
    """
    if isinstance(exc, (ProtectedError, RestrictedError)):
        objects = exc.protected_objects if isinstance(exc, ProtectedError) else exc.restricted_objects
        set_rollback()
        return Response(
            {
                'detail': 'This record is still referenced and cannot be deleted.',
                'referenced_by': sorted({str(obj._meta.verbose_name_plural) for obj in objects}),
            },
            status=status.HTTP_409_CONFLICT,
        )
    return drf_exception_handler(exc, context)
