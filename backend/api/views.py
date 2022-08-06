from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

import csv
import codecs

from .serializers import CustomTokenObtainPairSerializer

from accounts.serializers import MemberSerializer, RegisterMemberSerializer, WorkingGroupSerializer
from accounts.models import Member, WorkingGroup
from accounts.permissions import CompoundUserWritePermission

from chemicals.serializers import SubstanceSerializer, CompoundSerializer, ContainerSerializer
from chemicals.models import Substance, Compound, Container

from ghs.serializers import GHSSerializer





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CompoundList(request):
    queryset = Container.objects.all()
    serializer = ContainerSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
@permission_classes([CompoundUserWritePermission])
def CompoundDetail(request, pk):
    queryset = Compound.objects.get(pk=pk)
    serializer = CompoundSerializer(queryset)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SubstanceList(request):
    queryset = Substance.objects.all()
    serializer = SubstanceSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SubstanceDetail(request, pk):
    queryset = Substance.objects.get(pk=pk)
    serializer = SubstanceSerializer(queryset)
    return Response(serializer.data)


# AUTHENTICATION
# todo: use function based views
@permission_classes([])
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([])
def GroupList(request):
    queryset = WorkingGroup.objects.all()
    serializer = WorkingGroupSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserList(request):
    queryset = Member.objects.all()
    serializer = MemberSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([])
def RegisterUser(request):
    serializer = RegisterMemberSerializer(data=request.data)
    if serializer.is_valid():
        newuser = serializer.save()
        if newuser:
            # todo: something missing?
            pass
    return Response(serializer.data)


class CustomViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    # queryset = Model.objects.all()
    # model = queryset.model
    # serializer_class = ModelSerializer

    # permission_classes = []

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            self.model.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        item = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid():
            # check if changed field has permission:
            def has_changed(field_name):
                previous = self.get_queryset().get(pk=pk)
                changed = item[field_name] == serializer.validated_data[field_name]
                return changed
            # if has_changed(field_name):
            #     has_permission ? (depends on role)
            # todo: update roles (hard coded?)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, pk=pk, **kwargs)
        # item = get_object_or_404(self.get_queryset(), pk=pk)
        # serializer = self.serializer_class(item, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item = get_object_or_404(self.get_queryset(), pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[])
    def download_csv_template(self, request):
        model_fields = self.model._meta.fields + self.model._meta.many_to_many
        field_names = [field.name for field in model_fields if field.name != 'id']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}_template.csv"'

        # the csv writer
        writer = csv.writer(response, delimiter=";")
        # Write a first row with header information
        writer.writerow(field_names)
        return response

    @action(detail=False, methods=['get'])  # , permission_classes=[IsAdminUser])
    def download_csv(self, request):
        model_fields = self.model._meta.fields + self.model._meta.many_to_many
        field_names = [field.name for field in model_fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}.csv"'

        writer = csv.writer(response, delimiter=";")
        # Write a first row with header information
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
        if serializer.is_valid() and headers.issubset(field_names):
            item_list = [
                self.model(**{field: row[field] for field in headers}) for row in serializer.data
            ]
            self.model.objects.bulk_create(item_list)
            return Response(serializer.data)
        return Response(serializer.errors)

        # writing create methods for nested representations:
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
