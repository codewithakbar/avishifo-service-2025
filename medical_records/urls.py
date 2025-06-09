from django.urls import path
from .views import (
    MedicalRecordListView, MedicalRecordDetailView,
    MedicalRecordAttachmentView
)

urlpatterns = [
    path('', MedicalRecordListView.as_view(), name='medical-record-list'),
    path('<int:pk>/', MedicalRecordDetailView.as_view(), name='medical-record-detail'),
    path('<int:medical_record_id>/attachments/', MedicalRecordAttachmentView.as_view(), name='medical-record-attachments'),
]
