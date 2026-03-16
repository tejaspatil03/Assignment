"""
ProductCourseMapping URL configuration.
"""
from django.urls import path
from .views import ProductCourseMappingListView, ProductCourseMappingDetailView

urlpatterns = [
    path('product-course-mappings/', ProductCourseMappingListView.as_view(), name='product-course-mapping-list'),
    path('product-course-mappings/<int:pk>/', ProductCourseMappingDetailView.as_view(), name='product-course-mapping-detail'),
]
