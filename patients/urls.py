from django.urls import path
from .views import (
    PatientListView, PatientDetailView, PatientCreateView,
    patient_medical_summary
)

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('create/', PatientCreateView.as_view(), name='patient-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<int:pk>/medical-summary/', patient_medical_summary, name='patient-medical-summary'),
]
