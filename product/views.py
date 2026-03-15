from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer
from core.utils import get_object_or_404_custom


class ProductListCreateView(APIView):
    """
    get: List all products. Supports ?is_active= and ?vendor_id= filtering.
    post: Create a new product.
    """

    @swagger_auto_schema(
        operation_summary="List all products",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('vendor_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Filter products mapped to a specific vendor"),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        products = Product.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            products = products.filter(is_active=is_active.lower() == 'true')

        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            products = products.filter(
                vendorproductmapping__vendor_id=vendor_id,
                vendorproductmapping__is_active=True
            ).distinct()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a product", responses={200: ProductSerializer})
    def get(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        return Response(ProductSerializer(product).data)

    @swagger_auto_schema(operation_summary="Full update a product",
                         request_body=ProductSerializer, responses={200: ProductSerializer})
    def put(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a product",
                         request_body=ProductSerializer, responses={200: ProductSerializer})
    def patch(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft-delete a product", responses={204: "No Content"})
    def delete(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        product.is_active = False
        product.save()
        return Response({"message": "Product deactivated."}, status=status.HTTP_204_NO_CONTENT)
