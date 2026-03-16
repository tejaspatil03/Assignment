"""
VendorProductMapping URL configuration.
"""
from django.urls import path
from .views import VendorProductMappingListView, VendorProductMappingDetailView

urlpatterns = [
    path('vendor-product-mappings/', VendorProductMappingListView.as_view(), name='vendor-product-mapping-list'),
    path('vendor-product-mappings/<int:pk>/', VendorProductMappingDetailView.as_view(), name='vendor-product-mapping-detail'),
]
