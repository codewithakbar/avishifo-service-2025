from django.urls import path
from .views import (
    DoctorListView, DoctorDetailView, DoctorCreateView,
    doctor_dashboard_stats, doctor_schedule, doctor_specialties_list, doctor_specialties_with_stats
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('specialties/', doctor_specialties_list, name='doctor-specialties'),
    path('specialties/stats/', doctor_specialties_with_stats, name='doctor-specialties-stats'),  # С статистикой
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('<int:pk>/stats/', doctor_dashboard_stats, name='doctor-stats'),
    path('<int:pk>/schedule/', doctor_schedule, name='doctor-schedule'),
]