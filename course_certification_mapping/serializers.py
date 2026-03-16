"""
CourseCertificationMapping serializers.
"""
from rest_framework import serializers
from .models import CourseCertificationMapping
from course.models import Course
from certification.models import Certification


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseCertificationMapping model.
    """
    course_name = serializers.CharField(source='course.name', read_only=True)
    certification_name = serializers.CharField(source='certification.name', read_only=True)
    
    class Meta:
        model = CourseCertificationMapping
        fields = [
            'id', 'course', 'course_name', 'certification', 'certification_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'course_name', 'certification_name']

    def validate_course(self, value):
        """Validate that course exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Course is not active.")
        return value

    def validate_certification(self, value):
        """Validate that certification exists and is active."""
        if not value.is_active:
            raise serializers.ValidationError("Certification is not active.")
        return value

    def validate(self, data):
        """
        Validate the mapping data.
        - Check for duplicate mappings
        - Ensure only one primary mapping per course
        """
        course = data.get('course')
        certification = data.get('certification')
        primary_mapping = data.get('primary_mapping', False)
        
        # Check for duplicate mapping (course + certification combination)
        instance = getattr(self, 'instance', None)
        duplicate_query = CourseCertificationMapping.objects.filter(
            course=course,
            certification=certification
        )
        if instance:
            duplicate_query = duplicate_query.exclude(pk=instance.pk)
        
        if duplicate_query.exists():
            raise serializers.ValidationError(
                "A mapping between this course and certification already exists."
            )
        
        # Check primary mapping constraint
        if primary_mapping:
            primary_query = CourseCertificationMapping.objects.filter(
                course=course,
                primary_mapping=True,
                is_active=True
            )
            if instance:
                primary_query = primary_query.exclude(pk=instance.pk)
            
            if primary_query.exists():
                raise serializers.ValidationError(
                    "This course already has a primary certification mapping."
                )
        
        return data
