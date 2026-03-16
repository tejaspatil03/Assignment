"""
Product serializers.
"""
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        """Validate that name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def validate_code(self, value):
        """Validate that code is unique and not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Code is required.")
        value = value.strip()
        
        # Check uniqueness (excluding current instance on update)
        instance = getattr(self, 'instance', None)
        queryset = Product.objects.filter(code__iexact=value)
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A product with this code already exists.")
        return value
