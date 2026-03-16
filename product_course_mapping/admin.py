"""
ProductCourseMapping admin configuration.
"""
from django.contrib import admin
from .models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'primary_mapping', 'created_at', 'product']
    search_fields = ['product__name', 'course__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
