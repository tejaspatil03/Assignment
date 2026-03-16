"""
CourseCertificationMapping URL configuration.
"""
from django.urls import path
from .views import CourseCertificationMappingListView, CourseCertificationMappingDetailView

urlpatterns = [
    path('course-certification-mappings/', CourseCertificationMappingListView.as_view(), name='course-certification-mapping-list'),
    path('course-certification-mappings/<int:pk>/', CourseCertificationMappingDetailView.as_view(), name='course-certification-mapping-detail'),
]
