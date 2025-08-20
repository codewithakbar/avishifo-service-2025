from django.urls import path
from .views import (
    DoctorListView, DoctorDetailView, DoctorCreateView, DoctorProfileAPIView, DoctorProfileView, SpecialtyChoicesAPIView,
    doctor_dashboard_stats, doctor_schedule, doctor_specialties_list,
    doctor_specialties_with_stats, DoctorScheduleListView, DoctorScheduleDetailView,
    DoctorProfileManagementView, doctor_profile_fields_info
)

urlpatterns = [
    # Main doctor endpoints
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('create/', DoctorCreateView.as_view(), name='doctor-create'),
    
    # Profile management endpoints (MUST come before dynamic pk patterns)
    path('profile/', DoctorProfileManagementView.as_view(), name='doctor-profile-management'),
    path('profile/fields/', doctor_profile_fields_info, name='doctor-profile-fields-info'),
    path('profile/view/', DoctorProfileView.as_view(), name='doctor-profile-view'),
    path('doctor/profile/', DoctorProfileAPIView.as_view(), name='doctor-profile-api'),
    
    # Specialty endpoints
    path('specialties/', doctor_specialties_list, name='doctor-specialties'),
    path('specialties/stats/', doctor_specialties_with_stats, name='doctor-specialties-stats'),
    path('specialties/choices/', SpecialtyChoicesAPIView.as_view(), name='specialty-choices'),
    
    # Doctor specific endpoints (dynamic pk patterns - MUST come after static patterns)
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('<int:pk>/stats/', doctor_dashboard_stats, name='doctor-stats'),
    
    # Doctor Schedule URLs
    path('<int:doctor_pk>/schedule/', doctor_schedule, name='doctor-schedule'),
    path('<int:doctor_pk>/schedules/', DoctorScheduleListView.as_view(), name='doctor-schedules-list'),
    path('<int:doctor_pk>/schedules/<int:pk>/', DoctorScheduleDetailView.as_view(), name='doctor-schedules-detail'),
]