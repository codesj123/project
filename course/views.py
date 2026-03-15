from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course
from .serializers import CourseSerializer
from core.utils import get_object_or_404_custom


class CourseListCreateView(APIView):
    """
    get: List all courses. Supports ?is_active= and ?product_id= filtering.
    post: Create a new course.
    """

    @swagger_auto_schema(
        operation_summary="List all courses",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Filter courses mapped to a specific product"),
        ],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        courses = Course.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            courses = courses.filter(is_active=is_active.lower() == 'true')

        product_id = request.query_params.get('product_id')
        if product_id:
            courses = courses.filter(
                productcoursemapping__product_id=product_id,
                productcoursemapping__is_active=True
            ).distinct()

        return Response(CourseSerializer(courses, many=True).data)

    @swagger_auto_schema(
        operation_summary="Create a course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a course", responses={200: CourseSerializer})
    def get(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        return Response(CourseSerializer(course).data)

    @swagger_auto_schema(operation_summary="Full update a course",
                         request_body=CourseSerializer, responses={200: CourseSerializer})
    def put(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a course",
                         request_body=CourseSerializer, responses={200: CourseSerializer})
    def patch(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft-delete a course", responses={204: "No Content"})
    def delete(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        course.is_active = False
        course.save()
        return Response({"message": "Course deactivated."}, status=status.HTTP_204_NO_CONTENT)
