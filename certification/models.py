"""
Certification model definition.
"""
from django.db import models
from core.models import BaseModel


class Certification(BaseModel):
    """
    Certification master entity.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'certifications'
        ordering = ['-created_at']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return f"{self.name} ({self.code})"
