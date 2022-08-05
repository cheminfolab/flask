from django.shortcuts import render

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from rest_framework import viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import csv

from .models import *
from .serializers import *

fs = FileSystemStorage(location='tmp/')


# https://github.com/jha-shubham01/populate-data-using-csv
# https://www.youtube.com/watch?v=UKE5yQAmg0k

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def BuildingList(request):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer(queryset, many=True)

    # todo: revise !!!
    if request.method == 'POST':
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)

        product_list = []
        for id_, row in enumerate(reader):
            (name, address, city, state, zipcode, country) = row
            product_list.append(
                Building(
                    name=name,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode,
                    country=country
                )
            )

        Building.objects.bulk_create(product_list)
        return Response(serializer_class.data)

    return Response(serializer_class.data)

# # Viewset
# class BuildingList2(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for viewing and editing Product.
#     """
#     queryset = Building.objects.all()
#     serializer_class = BuildingSerializer
#
#     @action(detail=False, methods=['POST'])
#     def upload_data(self, request):
#         """Upload data from CSV"""
#         file = request.FILES["file"]
#
#         content = file.read()  # these are bytes
#         file_content = ContentFile(content)
#         file_name = fs.save(
#             "_tmp.csv", file_content
#         )
#         tmp_file = fs.path(file_name)
#
#         csv_file = open(tmp_file, errors="ignore")
#         reader = csv.reader(csv_file)
#         next(reader)
#
#         product_list = []
#         for id_, row in enumerate(reader):
#             (name, address, city, state, zipcode, country) = row
#             product_list.append(
#                 Building(
#                     name=name,
#                     address=address,
#                     city=city,
#                     state=state,
#                     zipcode=zipcode,
#                     country=country
#                 )
#             )
#
#         Building.objects.bulk_create(product_list)
#
#         return Response("Successfully upload the data")

# @action(detail=False, methods=['POST'])
# def upload_data_with_validation(self, request):
#     """Upload data from CSV, with validation."""
#     file = request.FILES.get("file")
#
#     reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
#     data = list(reader)
#
#     serializer = self.serializer_class(data=data, many=True)
#     serializer.is_valid(raise_exception=True)
#
#     product_list = []
#     for row in serializer.data:
#         product_list.append(
#             Product(
#                 user_id=row["user"],
#                 category=row["category"],
#                 price=row["price"],
#                 name=row["name"],
#                 description=row["description"],
#                 quantity=row["quantity"],
#             )
#         )
#
#     Product.objects.bulk_create(product_list)
#
#     return Response("Successfully upload the data")
