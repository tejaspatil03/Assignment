"""
ProductCourseMapping serializers.
"""
from rest_framework import serializers
from .models import ProductCourseMapping
from product.models import Product
from course.models import Course


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCourseMapping model.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = ProductCourseMapping
        fields = [
            'id', 'product', 'product_name', 'course', 'course_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'product_name', 'course_name']

    def validate_product(self, value):
        """Validate that product exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Product is not active.")
        return value

    def validate_course(self, value):
        """Validate that course exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Course is not active.")
        return value

    def validate(self, data):
        """
        Validate the mapping data.
        - Check for duplicate mappings
        - Ensure only one primary mapping per product
        """
        product = data.get('product')
        course = data.get('course')
        primary_mapping = data.get('primary_mapping', False)
        
        # Check for duplicate mapping (product + course combination)
        instance = getattr(self, 'instance', None)
        duplicate_query = ProductCourseMapping.objects.filter(
            product=product,
            course=course
        )
        if instance:
            duplicate_query = duplicate_query.exclude(pk=instance.pk)
        
        if duplicate_query.exists():
            raise serializers.ValidationError(
                "A mapping between this product and course already exists."
            )
        
        # Check primary mapping constraint
        if primary_mapping:
            primary_query = ProductCourseMapping.objects.filter(
                product=product,
                primary_mapping=True,
                is_active=True
            )
            if instance:
                primary_query = primary_query.exclude(pk=instance.pk)
            
            if primary_query.exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping."
                )
        
        return data
