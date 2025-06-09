from rest_framework import serializers
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from .models import MedicalRecord, MedicalRecordAttachment

class MedicalRecordAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecordAttachment
        fields = '__all__'
        read_only_fields = ('uploaded_at',)

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    attachments = MedicalRecordAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = (
            'patient', 'appointment', 'chief_complaint', 'history_of_present_illness',
            'physical_examination', 'diagnosis', 'treatment', 'prescription',
            'blood_pressure', 'heart_rate', 'temperature', 'respiratory_rate',
            'oxygen_saturation', 'follow_up_required', 'follow_up_date', 'notes'
        )

class MedicalRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = (
            'chief_complaint', 'history_of_present_illness', 'physical_examination',
            'diagnosis', 'treatment', 'prescription', 'blood_pressure', 'heart_rate',
            'temperature', 'respiratory_rate', 'oxygen_saturation',
            'follow_up_required', 'follow_up_date', 'notes'
        )
