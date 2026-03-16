"""
VendorProductMapping model definition.
"""
from django.db import models
from core.models import BaseModel
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(BaseModel):
    """
    Mapping between Vendor and Product.
    Only one primary mapping allowed per vendor.
    """
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='product_mappings'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='vendor_mappings'
    )
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendor_product_mappings'
        ordering = ['-created_at']
        verbose_name = 'Vendor Product Mapping'
        verbose_name_plural = 'Vendor Product Mappings'
        unique_together = ['vendor', 'product']  # Prevent duplicate mappings

    def __str__(self):
        return f"{self.vendor.name} -> {self.product.name} (Primary: {self.primary_mapping})"
