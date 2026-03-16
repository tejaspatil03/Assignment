"""
ProductCourseMapping model definition.
"""
from django.db import models
from core.models import BaseModel
from product.models import Product
from course.models import Course


class ProductCourseMapping(BaseModel):
    """
    Mapping between Product and Course.
    Only one primary mapping allowed per product.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='course_mappings'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='product_mappings'
    )
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_course_mappings'
        ordering = ['-created_at']
        verbose_name = 'Product Course Mapping'
        verbose_name_plural = 'Product Course Mappings'
        unique_together = ['product', 'course']  # Prevent duplicate mappings

    def __str__(self):
        return f"{self.product.name} -> {self.course.name} (Primary: {self.primary_mapping})"
