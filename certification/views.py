"""
Certification API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Certification
from .serializers import CertificationSerializer
from core.utils import get_object_or_404_custom


class CertificationListView(APIView):
    """
    List all certifications or create a new certification.
    Supports filtering by course_id via query parameter.
    """

    @swagger_auto_schema(
        operation_description="Get all certifications. Filter by course_id using ?course_id=1",
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description="Filter certifications by course ID",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: CertificationSerializer(many=True),
            400: openapi.Response(description="Bad request - invalid course_id"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all certifications with optional course_id filter."""
        course_id = request.query_params.get('course_id')
        
        if course_id:
            try:
                course_id = int(course_id)
                # Import here to avoid circular imports
                from course_certification_mapping.models import CourseCertificationMapping
                certification_ids = CourseCertificationMapping.objects.filter(
                    course_id=course_id,
                    is_active=True
                ).values_list('certification_id', flat=True)
                certifications = Certification.objects.filter(id__in=certification_ids, is_active=True)
            except ValueError:
                return Response(
                    {"error": "Invalid course_id. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            certifications = Certification.objects.filter(is_active=True)
            
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new certification",
        request_body=CertificationSerializer,
        responses={
            201: CertificationSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new certification."""
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailView(APIView):
    """
    Retrieve, update or delete a certification instance.
    """

    @swagger_auto_schema(
        operation_description="Get a certification by ID",
        responses={
            200: CertificationSerializer,
            404: openapi.Response(description="Certification not found")
        }
    )
    def get(self, request, pk):
        """Get a certification by ID."""
        certification, error_response = get_object_or_404_custom(Certification, pk, "Certification")
        if error_response:
            return error_response
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a certification completely",
        request_body=CertificationSerializer,
        responses={
            200: CertificationSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Certification not found")
        }
    )
    def put(self, request, pk):
        """Update a certification completely."""
        certification, error_response = get_object_or_404_custom(Certification, pk, "Certification")
        if error_response:
            return error_response
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a certification partially",
        request_body=CertificationSerializer,
        responses={
            200: CertificationSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Certification not found")
        }
    )
    def patch(self, request, pk):
        """Update a certification partially."""
        certification, error_response = get_object_or_404_custom(Certification, pk, "Certification")
        if error_response:
            return error_response
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a certification (sets is_active=False)",
        responses={
            204: openapi.Response(description="Certification soft deleted successfully"),
            404: openapi.Response(description="Certification not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a certification (sets is_active=False)."""
        certification, error_response = get_object_or_404_custom(Certification, pk, "Certification")
        if error_response:
            return error_response
        certification.is_active = False
        certification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
