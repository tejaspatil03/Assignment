"""
CourseCertificationMapping API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer
from core.utils import get_object_or_404_custom


class CourseCertificationMappingListView(APIView):
    """
    List all course-certification mappings or create a new mapping.
    Supports filtering by course_id via query parameter.
    """

    @swagger_auto_schema(
        operation_description="Get all course-certification mappings. Filter by course_id using ?course_id=1",
        manual_parameters=[
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description="Filter mappings by course ID",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: CourseCertificationMappingSerializer(many=True),
            400: openapi.Response(description="Bad request - invalid course_id"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all course-certification mappings with optional course_id filter."""
        course_id = request.query_params.get('course_id')
        
        queryset = CourseCertificationMapping.objects.filter(is_active=True)
        
        if course_id:
            try:
                course_id = int(course_id)
                queryset = queryset.filter(course_id=course_id)
            except ValueError:
                return Response(
                    {"error": "Invalid course_id. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        serializer = CourseCertificationMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={
            201: CourseCertificationMappingSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new course-certification mapping."""
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailView(APIView):
    """
    Retrieve, update or delete a course-certification mapping instance.
    """

    @swagger_auto_schema(
        operation_description="Get a course-certification mapping by ID",
        responses={
            200: CourseCertificationMappingSerializer,
            404: openapi.Response(description="Mapping not found")
        }
    )
    def get(self, request, pk):
        """Get a course-certification mapping by ID."""
        mapping, error_response = get_object_or_404_custom(
            CourseCertificationMapping, pk, "CourseCertificationMapping"
        )
        if error_response:
            return error_response
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a course-certification mapping completely",
        request_body=CourseCertificationMappingSerializer,
        responses={
            200: CourseCertificationMappingSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def put(self, request, pk):
        """Update a course-certification mapping completely."""
        mapping, error_response = get_object_or_404_custom(
            CourseCertificationMapping, pk, "CourseCertificationMapping"
        )
        if error_response:
            return error_response
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a course-certification mapping partially",
        request_body=CourseCertificationMappingSerializer,
        responses={
            200: CourseCertificationMappingSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def patch(self, request, pk):
        """Update a course-certification mapping partially."""
        mapping, error_response = get_object_or_404_custom(
            CourseCertificationMapping, pk, "CourseCertificationMapping"
        )
        if error_response:
            return error_response
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a course-certification mapping (sets is_active=False)",
        responses={
            204: openapi.Response(description="Mapping soft deleted successfully"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a course-certification mapping (sets is_active=False)."""
        mapping, error_response = get_object_or_404_custom(
            CourseCertificationMapping, pk, "CourseCertificationMapping"
        )
        if error_response:
            return error_response
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
