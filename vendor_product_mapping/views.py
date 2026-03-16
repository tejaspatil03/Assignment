"""
VendorProductMapping API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer
from core.utils import get_object_or_404_custom


class VendorProductMappingListView(APIView):
    """
    List all vendor-product mappings or create a new mapping.
    Supports filtering by vendor_id via query parameter.
    """

    @swagger_auto_schema(
        operation_description="Get all vendor-product mappings. Filter by vendor_id using ?vendor_id=1",
        manual_parameters=[
            openapi.Parameter(
                'vendor_id',
                openapi.IN_QUERY,
                description="Filter mappings by vendor ID",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: VendorProductMappingSerializer(many=True),
            400: openapi.Response(description="Bad request - invalid vendor_id"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all vendor-product mappings with optional vendor_id filter."""
        vendor_id = request.query_params.get('vendor_id')
        
        queryset = VendorProductMapping.objects.filter(is_active=True)
        
        if vendor_id:
            try:
                vendor_id = int(vendor_id)
                queryset = queryset.filter(vendor_id=vendor_id)
            except ValueError:
                return Response(
                    {"error": "Invalid vendor_id. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        serializer = VendorProductMappingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={
            201: VendorProductMappingSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new vendor-product mapping."""
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailView(APIView):
    """
    Retrieve, update or delete a vendor-product mapping instance.
    """

    @swagger_auto_schema(
        operation_description="Get a vendor-product mapping by ID",
        responses={
            200: VendorProductMappingSerializer,
            404: openapi.Response(description="Mapping not found")
        }
    )
    def get(self, request, pk):
        """Get a vendor-product mapping by ID."""
        mapping, error_response = get_object_or_404_custom(
            VendorProductMapping, pk, "VendorProductMapping"
        )
        if error_response:
            return error_response
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a vendor-product mapping completely",
        request_body=VendorProductMappingSerializer,
        responses={
            200: VendorProductMappingSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def put(self, request, pk):
        """Update a vendor-product mapping completely."""
        mapping, error_response = get_object_or_404_custom(
            VendorProductMapping, pk, "VendorProductMapping"
        )
        if error_response:
            return error_response
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a vendor-product mapping partially",
        request_body=VendorProductMappingSerializer,
        responses={
            200: VendorProductMappingSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def patch(self, request, pk):
        """Update a vendor-product mapping partially."""
        mapping, error_response = get_object_or_404_custom(
            VendorProductMapping, pk, "VendorProductMapping"
        )
        if error_response:
            return error_response
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a vendor-product mapping (sets is_active=False)",
        responses={
            204: openapi.Response(description="Mapping soft deleted successfully"),
            404: openapi.Response(description="Mapping not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a vendor-product mapping (sets is_active=False)."""
        mapping, error_response = get_object_or_404_custom(
            VendorProductMapping, pk, "VendorProductMapping"
        )
        if error_response:
            return error_response
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
