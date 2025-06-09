from rest_framework import serializers
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'fee')

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'patient', 'doctor', 'appointment_date', 'appointment_type',
            'reason', 'duration_minutes'
        )
    
    def validate_appointment_date(self, value):
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError("Appointment date must be in the future")
        return value

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'appointment_date', 'appointment_type', 'status',
            'reason', 'notes', 'duration_minutes'
        )
