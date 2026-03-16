"""
CourseCertificationMapping admin configuration.
"""
from django.contrib import admin
from .models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'primary_mapping', 'created_at', 'course']
    search_fields = ['course__name', 'certification__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
