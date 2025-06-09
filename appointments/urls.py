from django.urls import path
from .views import (
    AppointmentListView, AppointmentDetailView,
    cancel_appointment, upcoming_appointments
)

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:pk>/cancel/', cancel_appointment, name='cancel-appointment'),
    path('upcoming/', upcoming_appointments, name='upcoming-appointments'),
]
