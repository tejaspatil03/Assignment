"""
Vendor model definition.
"""
from django.db import models
from core.models import BaseModel


class Vendor(BaseModel):
    """
    Vendor master entity.
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendors'
        ordering = ['-created_at']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return f"{self.name} ({self.code})"
