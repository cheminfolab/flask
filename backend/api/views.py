import codecs
import csv

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import TrackedModel
from .permissions import ReadOnlyOrAdmin

CSV_DELIMITER = ';'
# Cells starting with these characters are executed as formulas by spreadsheet programs.
FORMULA_PREFIXES = ('=', '+', '-', '@', '\t', '\r')


def escape_csv_text(value):
    if isinstance(value, str) and value.startswith(FORMULA_PREFIXES):
        return "'" + value
    return value


def unescape_csv_text(value):
    if isinstance(value, str) and value.startswith("'") and value[1:].startswith(FORMULA_PREFIXES):
        return value[1:]
    return value


class CsvMixin:
    """
    CSV template, export and import for a ModelViewSet.

    Format: ';'-separated, UTF-8, one header row of field names. Foreign keys are
    written as primary keys, many-to-many fields as comma-separated primary keys.
    Import validates every row with the viewset's serializer and saves all rows
    or none (the request runs in a transaction, see ATOMIC_REQUESTS).
    """

    def _csv_model(self):
        return self.get_queryset().model

    def _csv_response(self, filename):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def _writable_field_names(self):
        serializer = self.get_serializer()
        return [name for name, field in serializer.fields.items() if not field.read_only]

    @action(detail=False, methods=['get'])
    def download_csv_template(self, request):
        model = self._csv_model()
        response = self._csv_response(f'{model._meta.model_name}_template.csv')
        csv.writer(response, delimiter=CSV_DELIMITER).writerow(self._writable_field_names())
        return response

    @action(detail=False, methods=['get'])
    def download_csv(self, request):
        model = self._csv_model()
        concrete = [field for field in model._meta.concrete_fields]
        many_to_many = list(model._meta.many_to_many)
        response = self._csv_response(f'{model._meta.model_name}.csv')
        writer = csv.writer(response, delimiter=CSV_DELIMITER)
        writer.writerow([field.name for field in concrete + many_to_many])

        queryset = self.get_queryset().prefetch_related(*[field.name for field in many_to_many])
        for row in queryset.iterator(chunk_size=500):
            values = []
            for field in concrete:
                value = getattr(row, field.attname)  # FK -> primary key
                values.append('' if value is None else escape_csv_text(value))
            for field in many_to_many:
                values.append(','.join(str(pk) for pk in getattr(row, field.name).values_list('pk', flat=True)))
            writer.writerow(values)
        return response

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        upload = request.FILES.get('file')
        if upload is None:
            raise ValidationError({'file': ['No file uploaded (multipart field "file").']})

        try:
            reader = csv.DictReader(codecs.iterdecode(upload, 'utf-8'), delimiter=CSV_DELIMITER)
            headers = reader.fieldnames or []
            unknown = set(headers) - set(self._writable_field_names())
            if unknown:
                raise ValidationError({'file': [f'Unknown or read-only columns: {", ".join(sorted(unknown))}']})
            many_to_many = {field.name for field in self._csv_model()._meta.many_to_many}
            rows = []
            for raw in reader:
                row = {}
                for key, value in raw.items():
                    if key in many_to_many:
                        row[key] = [item for item in (value or '').split(',') if item]
                    elif value != '':
                        row[key] = unescape_csv_text(value)
                rows.append(row)
        except UnicodeDecodeError:
            raise ValidationError({'file': ['File is not valid UTF-8.']})

        serializer = self.get_serializer(data=rows, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProvenanceMixin:
    """
    Provenance is assigned by the server: for TrackedModel subclasses,
    `created_by` / `updated_by` come from the authenticated user.
    """

    def _is_tracked(self):
        return issubclass(self.get_queryset().model, TrackedModel)

    def perform_create(self, serializer, **extra):
        if self._is_tracked():
            extra.setdefault('created_by', self.request.user)
            extra.setdefault('updated_by', self.request.user)
        serializer.save(**extra)

    def perform_update(self, serializer, **extra):
        if self._is_tracked():
            extra['updated_by'] = self.request.user
        serializer.save(**extra)


class BaseModelViewSet(CsvMixin, ProvenanceMixin, ModelViewSet):
    """
    Standard CRUD viewset for reference and inventory data.

    - Deny by default: authenticated read access, staff-only writes
      (override `permission_classes` or `get_permissions` explicitly).
    - Server-assigned provenance (ProvenanceMixin).
    - Every request runs in a database transaction (ATOMIC_REQUESTS).
    """
    permission_classes = [ReadOnlyOrAdmin]
