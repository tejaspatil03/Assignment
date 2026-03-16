"""
VendorProductMapping serializers.
"""
from rest_framework import serializers
from .models import VendorProductMapping
from vendor.models import Vendor
from product.models import Product


class VendorProductMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for VendorProductMapping model.
    """
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = VendorProductMapping
        fields = [
            'id', 'vendor', 'vendor_name', 'product', 'product_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'vendor_name', 'product_name']

    def validate_vendor(self, value):
        """Validate that vendor exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Vendor is not active.")
        return value

    def validate_product(self, value):
        """Validate that product exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Product is not active.")
        return value

    def validate(self, data):
        """
        Validate the mapping data.
        - Check for duplicate mappings
        - Ensure only one primary mapping per vendor
        """
        vendor = data.get('vendor')
        product = data.get('product')
        primary_mapping = data.get('primary_mapping', False)
        
        # Check for duplicate mapping (vendor + product combination)
        instance = getattr(self, 'instance', None)
        duplicate_query = VendorProductMapping.objects.filter(
            vendor=vendor,
            product=product
        )
        if instance:
            duplicate_query = duplicate_query.exclude(pk=instance.pk)
        
        if duplicate_query.exists():
            raise serializers.ValidationError(
                "A mapping between this vendor and product already exists."
            )
        
        # Check primary mapping constraint
        if primary_mapping:
            primary_query = VendorProductMapping.objects.filter(
                vendor=vendor,
                primary_mapping=True,
                is_active=True
            )
            if instance:
                primary_query = primary_query.exclude(pk=instance.pk)
            
            if primary_query.exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product mapping."
                )
        
        return data
