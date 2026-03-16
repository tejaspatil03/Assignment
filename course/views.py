"""
Course API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course
from .serializers import CourseSerializer
from core.utils import get_object_or_404_custom


class CourseListView(APIView):
    """
    List all courses or create a new course.
    Supports filtering by product_id via query parameter.
    """

    @swagger_auto_schema(
        operation_description="Get all courses. Filter by product_id using ?product_id=1",
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter courses by product ID",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: CourseSerializer(many=True),
            400: openapi.Response(description="Bad request - invalid product_id"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all courses with optional product_id filter."""
        product_id = request.query_params.get('product_id')
        
        if product_id:
            try:
                product_id = int(product_id)
                # Import here to avoid circular imports
                from product_course_mapping.models import ProductCourseMapping
                course_ids = ProductCourseMapping.objects.filter(
                    product_id=product_id,
                    is_active=True
                ).values_list('course_id', flat=True)
                courses = Course.objects.filter(id__in=course_ids, is_active=True)
            except ValueError:
                return Response(
                    {"error": "Invalid product_id. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            courses = Course.objects.filter(is_active=True)
            
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new course."""
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """
    Retrieve, update or delete a course instance.
    """

    @swagger_auto_schema(
        operation_description="Get a course by ID",
        responses={
            200: CourseSerializer,
            404: openapi.Response(description="Course not found")
        }
    )
    def get(self, request, pk):
        """Get a course by ID."""
        course, error_response = get_object_or_404_custom(Course, pk, "Course")
        if error_response:
            return error_response
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a course completely",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Course not found")
        }
    )
    def put(self, request, pk):
        """Update a course completely."""
        course, error_response = get_object_or_404_custom(Course, pk, "Course")
        if error_response:
            return error_response
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a course partially",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Course not found")
        }
    )
    def patch(self, request, pk):
        """Update a course partially."""
        course, error_response = get_object_or_404_custom(Course, pk, "Course")
        if error_response:
            return error_response
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a course (sets is_active=False)",
        responses={
            204: openapi.Response(description="Course soft deleted successfully"),
            404: openapi.Response(description="Course not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a course (sets is_active=False)."""
        course, error_response = get_object_or_404_custom(Course, pk, "Course")
        if error_response:
            return error_response
        course.is_active = False
        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
