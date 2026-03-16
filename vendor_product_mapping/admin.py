"""
VendorProductMapping admin configuration.
"""
from django.contrib import admin
from .models import VendorProductMapping


@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'primary_mapping', 'created_at', 'vendor']
    search_fields = ['vendor__name', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
