from django.urls import path
from .views import (
    DoctorListView, DoctorDetailView, DoctorCreateView,
    doctor_dashboard_stats, doctor_schedule
)

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('<int:pk>/stats/', doctor_dashboard_stats, name='doctor-stats'),
    path('<int:pk>/schedule/', doctor_schedule, name='doctor-schedule'),
]
