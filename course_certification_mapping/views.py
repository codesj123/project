from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer
from core.utils import get_object_or_404_custom


class CourseCertificationMappingListCreateView(APIView):
    """
    get: List all course-certification mappings. Supports ?course_id= and ?certification_id= filtering.
    post: Create a new course-certification mapping.
    """

    @swagger_auto_schema(
        operation_summary="List course-certification mappings",
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('certification_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = CourseCertificationMapping.objects.all()

        course_id = request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course_id=course_id)

        certification_id = request.query_params.get('certification_id')
        if certification_id:
            qs = qs.filter(certification_id=certification_id)

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')

        return Response(CourseCertificationMappingSerializer(qs, many=True).data)

    @swagger_auto_schema(
        operation_summary="Create a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a course-certification mapping",
                         responses={200: CourseCertificationMappingSerializer})
    def get(self, request, pk):
        obj, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        return Response(CourseCertificationMappingSerializer(obj).data)

    @swagger_auto_schema(operation_summary="Full update a course-certification mapping",
                         request_body=CourseCertificationMappingSerializer,
                         responses={200: CourseCertificationMappingSerializer})
    def put(self, request, pk):
        obj, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        serializer = CourseCertificationMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a course-certification mapping",
                         request_body=CourseCertificationMappingSerializer,
                         responses={200: CourseCertificationMappingSerializer})
    def patch(self, request, pk):
        obj, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        serializer = CourseCertificationMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft-delete a course-certification mapping",
                         responses={204: "No Content"})
    def delete(self, request, pk):
        obj, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Mapping deactivated."}, status=status.HTTP_204_NO_CONTENT)
