from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from core.utils import get_object_or_404_custom


class ProductCourseMappingListCreateView(APIView):
    """
    get: List all product-course mappings. Supports ?product_id= and ?course_id= filtering.
    post: Create a new product-course mapping.
    """

    @swagger_auto_schema(
        operation_summary="List product-course mappings",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = ProductCourseMapping.objects.all()

        product_id = request.query_params.get('product_id')
        if product_id:
            qs = qs.filter(product_id=product_id)

        course_id = request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course_id=course_id)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')

        return Response(ProductCourseMappingSerializer(qs, many=True).data)

    @swagger_auto_schema(
        operation_summary="Create a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a product-course mapping",
                         responses={200: ProductCourseMappingSerializer})
    def get(self, request, pk):
        obj, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        return Response(ProductCourseMappingSerializer(obj).data)

    @swagger_auto_schema(operation_summary="Full update a product-course mapping",
                         request_body=ProductCourseMappingSerializer,
                         responses={200: ProductCourseMappingSerializer})
    def put(self, request, pk):
        obj, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        serializer = ProductCourseMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a product-course mapping",
                         request_body=ProductCourseMappingSerializer,
                         responses={200: ProductCourseMappingSerializer})
    def patch(self, request, pk):
        obj, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        serializer = ProductCourseMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft-delete a product-course mapping",
                         responses={204: "No Content"})
    def delete(self, request, pk):
        obj, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Mapping deactivated."}, status=status.HTTP_204_NO_CONTENT)
