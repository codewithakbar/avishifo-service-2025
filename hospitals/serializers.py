from rest_framework import serializers
from .models import Hospital

class HospitalSerializer(serializers.ModelSerializer):
    total_doctors = serializers.ReadOnlyField()
    available_doctors = serializers.ReadOnlyField()
    
    class Meta:
        model = Hospital
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class HospitalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = (
            'name', 'address', 'phone_number', 'email', 'website',
            'license_number', 'established_date', 'bed_capacity',
            'emergency_services'
        )
