"""
CourseCertificationMapping model definition.
"""
from django.db import models
from core.models import BaseModel
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(BaseModel):
    """
    Mapping between Course and Certification.
    Only one primary mapping allowed per course.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certification_mappings'
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name='course_mappings'
    )
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'course_certification_mappings'
        ordering = ['-created_at']
        verbose_name = 'Course Certification Mapping'
        verbose_name_plural = 'Course Certification Mappings'
        unique_together = ['course', 'certification']  # Prevent duplicate mappings

    def __str__(self):
        return f"{self.course.name} -> {self.certification.name} (Primary: {self.primary_mapping})"
