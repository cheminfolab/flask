from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, HttpResponse

import csv
import codecs


class CustomViewSet(ViewSet):

    model = None
    serializer_class = None
    # permission_classes = []

    def get_queryset(self):
        return self.model.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(request, message=getattr(permission, 'message', None))

    def get_object(self, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # todo: problems with create user?
            self.model.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk=pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, **kwargs):
        kwargs['partial'] = True
        return self.update(request, pk=pk, **kwargs)

    def destroy(self, request, pk=None):
        instance = self.get_object(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def download_csv_template(self, request):
        model_fields = self.model._meta.fields + self.model._meta.many_to_many  # other relationships??
        field_names = [field.name for field in model_fields if field.name != 'id']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}_template.csv"'

        writer = csv.writer(response, delimiter=";")
        writer.writerow(field_names)
        return response

    @action(detail=False, methods=['get'])
    def download_csv(self, request):
        model_fields = self.model._meta.fields + self.model._meta.many_to_many
        field_names = [field.name for field in model_fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}.csv"'

        writer = csv.writer(response, delimiter=";")
        writer.writerow(field_names)
        # # Write data rows
        for row in self.get_queryset():
            values = []
            for field in field_names:
                value = getattr(row, field)
                if callable(value):
                    try:
                        value = value() or ''
                    except Exception as e:
                        value = f'Error retrieving value: {e}'
                if value is None:
                    value = ''
                values.append(value)
            writer.writerow(values)
        return response

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        model_fields = self.model._meta.fields + self.model._meta.many_to_many
        field_names = [field.name for field in model_fields]
        file = request.FILES['file']
        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        headers = reader.fieldnames
        serializer = self.serializer_class(data=data, many=True)
        if serializer.is_valid() and set(headers).issubset(set(field_names)):
            item_list = [
                self.model(**{field: row[field] for field in headers}) for row in serializer.data
            ]
            self.model.objects.bulk_create(item_list)
            return Response(serializer.data)
        return Response(serializer.errors)

        # writing create methods for nested representations:
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
