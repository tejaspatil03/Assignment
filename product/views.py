"""
Product API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer
from core.utils import get_object_or_404_custom


class ProductListView(APIView):
    """
    List all products or create a new product.
    Supports filtering by vendor_id via query parameter.
    """

    @swagger_auto_schema(
        operation_description="Get all products. Filter by vendor_id using ?vendor_id=1",
        manual_parameters=[
            openapi.Parameter(
                'vendor_id',
                openapi.IN_QUERY,
                description="Filter products by vendor ID",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: ProductSerializer(many=True),
            400: openapi.Response(description="Bad request - invalid vendor_id"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all products with optional vendor_id filter."""
        vendor_id = request.query_params.get('vendor_id')
        
        if vendor_id:
            try:
                vendor_id = int(vendor_id)
                # Import here to avoid circular imports
                from vendor_product_mapping.models import VendorProductMapping
                product_ids = VendorProductMapping.objects.filter(
                    vendor_id=vendor_id,
                    is_active=True
                ).values_list('product_id', flat=True)
                products = Product.objects.filter(id__in=product_ids, is_active=True)
            except ValueError:
                return Response(
                    {"error": "Invalid vendor_id. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            products = Product.objects.filter(is_active=True)
            
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new product."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Retrieve, update or delete a product instance.
    """

    @swagger_auto_schema(
        operation_description="Get a product by ID",
        responses={
            200: ProductSerializer,
            404: openapi.Response(description="Product not found")
        }
    )
    def get(self, request, pk):
        """Get a product by ID."""
        product, error_response = get_object_or_404_custom(Product, pk, "Product")
        if error_response:
            return error_response
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a product completely",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Product not found")
        }
    )
    def put(self, request, pk):
        """Update a product completely."""
        product, error_response = get_object_or_404_custom(Product, pk, "Product")
        if error_response:
            return error_response
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a product partially",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Product not found")
        }
    )
    def patch(self, request, pk):
        """Update a product partially."""
        product, error_response = get_object_or_404_custom(Product, pk, "Product")
        if error_response:
            return error_response
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a product (sets is_active=False)",
        responses={
            204: openapi.Response(description="Product soft deleted successfully"),
            404: openapi.Response(description="Product not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a product (sets is_active=False)."""
        product, error_response = get_object_or_404_custom(Product, pk, "Product")
        if error_response:
            return error_response
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
