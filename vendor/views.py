"""
Vendor API views using APIView.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vendor
from .serializers import VendorSerializer
from core.utils import get_object_or_404_custom


class VendorListView(APIView):
    """
    List all vendors or create a new vendor.
    """

    @swagger_auto_schema(
        operation_description="Get all vendors",
        responses={
            200: VendorSerializer(many=True),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request):
        """Get all vendors."""
        vendors = Vendor.objects.filter(is_active=True)
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={
            201: VendorSerializer,
            400: openapi.Response(description="Bad request - validation error")
        }
    )
    def post(self, request):
        """Create a new vendor."""
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    """
    Retrieve, update or delete a vendor instance.
    """

    @swagger_auto_schema(
        operation_description="Get a vendor by ID",
        responses={
            200: VendorSerializer,
            404: openapi.Response(description="Vendor not found")
        }
    )
    def get(self, request, pk):
        """Get a vendor by ID."""
        vendor, error_response = get_object_or_404_custom(Vendor, pk, "Vendor")
        if error_response:
            return error_response
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a vendor completely",
        request_body=VendorSerializer,
        responses={
            200: VendorSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Vendor not found")
        }
    )
    def put(self, request, pk):
        """Update a vendor completely."""
        vendor, error_response = get_object_or_404_custom(Vendor, pk, "Vendor")
        if error_response:
            return error_response
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a vendor partially",
        request_body=VendorSerializer,
        responses={
            200: VendorSerializer,
            400: openapi.Response(description="Bad request - validation error"),
            404: openapi.Response(description="Vendor not found")
        }
    )
    def patch(self, request, pk):
        """Update a vendor partially."""
        vendor, error_response = get_object_or_404_custom(Vendor, pk, "Vendor")
        if error_response:
            return error_response
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a vendor (sets is_active=False)",
        responses={
            204: openapi.Response(description="Vendor soft deleted successfully"),
            404: openapi.Response(description="Vendor not found")
        }
    )
    def delete(self, request, pk):
        """Soft delete a vendor (sets is_active=False)."""
        vendor, error_response = get_object_or_404_custom(Vendor, pk, "Vendor")
        if error_response:
            return error_response
        vendor.is_active = False
        vendor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
