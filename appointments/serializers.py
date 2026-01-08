# appointments/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Appointment
from accounts.serializers import UserSerializer

class AppointmentListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_age = serializers.SerializerMethodField()
    patient_phone = serializers.CharField(source='patient.phone_number', read_only=True)
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    
    def get_patient_age(self, obj):
        """Calculate patient age from date_of_birth"""
        return obj.patient_age
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient_name', 'patient_age', 'patient_phone', 'patient_email',
            'doctor_name', 'requested_date', 'requested_time', 'reason', 'description',
            'status', 'priority', 'patient_history_notes', 'confirmed_at', 'rejected_at',
            'rejection_reason', 'created_at', 'updated_at'
        ]

class AppointmentDetailSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    patient_age = serializers.SerializerMethodField()
    
    def get_patient_age(self, obj):
        """Calculate patient age from date_of_birth"""
        return obj.patient_age
    
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'doctor', 'requested_date', 'requested_time', 'reason', 'description',
            'priority', 'patient_phone', 'patient_email', 'patient_history_notes'
        ]
    
    def create(self, validated_data):
        # Automatically set patient from request user
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'status', 'rejection_reason', 'patient_history_notes'
        ]
    
    def update(self, instance, validated_data):
        # Set timestamps based on status changes
        if 'status' in validated_data:
            if validated_data['status'] == 'confirmed' and instance.status != 'confirmed':
                validated_data['confirmed_at'] = timezone.now()
            elif validated_data['status'] == 'rejected' and instance.status != 'rejected':
                validated_data['rejected_at'] = timezone.now()
        
        return super().update(instance, validated_data)