"""
ProductCourseMapping API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from core.utils import get_object_or_404_custom


class ProductCourseMappingListView(APIView):
    """
    List all product-course mappings or create a new mapping.
    Supports filtering by product_id via query parameter.
    """

    @swagger_auto_schema(
        operation_description="Get all product-course mappings. Filter by product_id using ?product_id=1",
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter mappings by product ID",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: ProductCourseMappingSerializer(many=True),
            400: openapi.Response(description="Bad request - invalid product_id"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all product-course mappings with optional product_id filter."""
        product_id = request.query_params.get('product_id')
        
        queryset = ProductCourseMapping.objects.filter(is_active=True)
        
        if product_id:
            try:
                product_id = int(product_id)
                queryset = queryset.filter(product_id=product_id)
            except ValueError:
                return Response(
                    {"error": "Invalid product_id. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        serializer = ProductCourseMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={
            201: ProductCourseMappingSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new product-course mapping."""
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):
    """
    Retrieve, update or delete a product-course mapping instance.
    """

    @swagger_auto_schema(
        operation_description="Get a product-course mapping by ID",
        responses={
            200: ProductCourseMappingSerializer,
            404: openapi.Response(description="Mapping not found")
        }
    )
    def get(self, request, pk):
        """Get a product-course mapping by ID."""
        mapping, error_response = get_object_or_404_custom(
            ProductCourseMapping, pk, "ProductCourseMapping"
        )
        if error_response:
            return error_response
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a product-course mapping completely",
        request_body=ProductCourseMappingSerializer,
        responses={
            200: ProductCourseMappingSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def put(self, request, pk):
        """Update a product-course mapping completely."""
        mapping, error_response = get_object_or_404_custom(
            ProductCourseMapping, pk, "ProductCourseMapping"
        )
        if error_response:
            return error_response
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a product-course mapping partially",
        request_body=ProductCourseMappingSerializer,
        responses={
            200: ProductCourseMappingSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def patch(self, request, pk):
        """Update a product-course mapping partially."""
        mapping, error_response = get_object_or_404_custom(
            ProductCourseMapping, pk, "ProductCourseMapping"
        )
        if error_response:
            return error_response
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a product-course mapping (sets is_active=False)",
        responses={
            204: openapi.Response(description="Mapping soft deleted successfully"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a product-course mapping (sets is_active=False)."""
        mapping, error_response = get_object_or_404_custom(
            ProductCourseMapping, pk, "ProductCourseMapping"
        )
        if error_response:
            return error_response
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
