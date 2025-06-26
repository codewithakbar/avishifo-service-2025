from django.urls import path
from .views import (
    DoctorListView, DoctorDetailView, DoctorCreateView, DoctorProfileAPIView, DoctorProfileView, SpecialtyChoicesAPIView,
    doctor_dashboard_stats, doctor_schedule, doctor_specialties_list,
    doctor_specialties_with_stats, DoctorScheduleListView, DoctorScheduleDetailView
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('specialties/', doctor_specialties_list, name='doctor-specialties'),
    path('specialties/stats/', doctor_specialties_with_stats, name='doctor-specialties-stats'),  # With stats
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('<int:pk>/stats/', doctor_dashboard_stats, name='doctor-stats'),
    
    # Doctor Schedule URLs
    path('<int:doctor_pk>/schedule/', doctor_schedule, name='doctor-schedule'), # Existing function-based view
    # You can use the class-based views for more RESTful approach if preferred:
    path('<int:doctor_pk>/schedules/', DoctorScheduleListView.as_view(), name='doctor-schedules-list'),
    path('<int:doctor_pk>/schedules/<int:pk>/', DoctorScheduleDetailView.as_view(), name='doctor-schedules-detail'),
    path('profile/', DoctorProfileView.as_view(), name='doctor-profile'),

    path('doctor/profile/', DoctorProfileAPIView.as_view(), name='doctor-profile'),
    path("specialties/", SpecialtyChoicesAPIView.as_view(), name="specialty-choices")

]