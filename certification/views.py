from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Certification
from .serializers import CertificationSerializer
from core.utils import get_object_or_404_custom


class CertificationListCreateView(APIView):
    """
    get: List all certifications. Supports ?is_active= and ?course_id= filtering.
    post: Create a new certification.
    """

    @swagger_auto_schema(
        operation_summary="List all certifications",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Filter certifications mapped to a specific course"),
        ],
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):
        certifications = Certification.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            certifications = certifications.filter(is_active=is_active.lower() == 'true')

        course_id = request.query_params.get('course_id')
        if course_id:
            certifications = certifications.filter(
                coursecertificationmapping__course_id=course_id,
                coursecertificationmapping__is_active=True
            ).distinct()

        return Response(CertificationSerializer(certifications, many=True).data)

    @swagger_auto_schema(
        operation_summary="Create a certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a certification",
                         responses={200: CertificationSerializer})
    def get(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        return Response(CertificationSerializer(cert).data)

    @swagger_auto_schema(operation_summary="Full update a certification",
                         request_body=CertificationSerializer, responses={200: CertificationSerializer})
    def put(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        serializer = CertificationSerializer(cert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a certification",
                         request_body=CertificationSerializer, responses={200: CertificationSerializer})
    def patch(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        serializer = CertificationSerializer(cert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft-delete a certification",
                         responses={204: "No Content"})
    def delete(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        cert.is_active = False
        cert.save()
        return Response({"message": "Certification deactivated."}, status=status.HTTP_204_NO_CONTENT)
