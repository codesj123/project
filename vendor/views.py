from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vendor
from .serializers import VendorSerializer
from core.utils import get_object_or_404_custom


class VendorListCreateView(APIView):
    """
    get: List all vendors (supports ?is_active= filter)
    post: Create a new vendor
    """

    @swagger_auto_schema(
        operation_summary="List all vendors",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                              description="Filter by active status"),
        ],
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            vendors = vendors.filter(is_active=is_active.lower() == 'true')
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    """
    get: Retrieve a vendor
    put: Full update a vendor
    patch: Partial update a vendor
    delete: Soft-delete a vendor
    """

    @swagger_auto_schema(operation_summary="Retrieve a vendor", responses={200: VendorSerializer})
    def get(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        return Response(VendorSerializer(vendor).data)

    @swagger_auto_schema(operation_summary="Full update a vendor",
                         request_body=VendorSerializer, responses={200: VendorSerializer})
    def put(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a vendor",
                         request_body=VendorSerializer, responses={200: VendorSerializer})
    def patch(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft-delete a vendor", responses={204: "No Content"})
    def delete(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        vendor.is_active = False
        vendor.save()
        return Response({"message": "Vendor deactivated."}, status=status.HTTP_204_NO_CONTENT)
