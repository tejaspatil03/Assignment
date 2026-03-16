"""
Vendor URL configuration.
"""
from django.urls import path
from .views import VendorListView, VendorDetailView

urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
]
