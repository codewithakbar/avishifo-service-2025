from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import MedicalRecord, MedicalRecordAttachment
from .serializers import (
    MedicalRecordSerializer, MedicalRecordCreateSerializer,
    MedicalRecordUpdateSerializer, MedicalRecordAttachmentSerializer
)

class MedicalRecordListView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'follow_up_required']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient':
            return MedicalRecord.objects.filter(patient__user=user)
        elif user.user_type == 'doctor':
            return MedicalRecord.objects.filter(doctor__user=user)
        else:
            return MedicalRecord.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MedicalRecordUpdateSerializer
        return MedicalRecordSerializer

class MedicalRecordAttachmentView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        medical_record_id = self.kwargs['medical_record_id']
        return MedicalRecordAttachment.objects.filter(medical_record_id=medical_record_id)
    
    def perform_create(self, serializer):
        medical_record_id = self.kwargs['medical_record_id']
        serializer.save(medical_record_id=medical_record_id)
