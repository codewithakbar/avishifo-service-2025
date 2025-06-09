from rest_framework import serializers
from accounts.serializers import UserSerializer
from hospitals.serializers import HospitalSerializer
from .models import Doctor, DoctorSchedule

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('doctor_id', 'rating', 'created_at', 'updated_at')

class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'specialty', 'license_number', 'hospital', 'years_of_experience',
            'education', 'certifications', 'consultation_fee'
        )

class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'specialty', 'years_of_experience', 'education',
            'certifications', 'consultation_fee', 'is_available'
        )
