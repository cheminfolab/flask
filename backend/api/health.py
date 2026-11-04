from django.db import connection
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response


@extend_schema(responses={
    200: inline_serializer('Health', {'status': serializers.CharField()}),
    503: inline_serializer('HealthFailure', {'status': serializers.CharField()}),
})
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
@throttle_classes([])
def health(request):
    """
    Liveness/readiness probe for Docker and load balancers: 200 when the
    application can reach the database, 503 otherwise. Reveals nothing else.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        return Response({'status': 'unavailable'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'status': 'ok'})
