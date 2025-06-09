from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('patient_id', 'created_at', 'updated_at')

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'blood_type', 'emergency_contact_name', 'emergency_contact_phone',
            'medical_history', 'allergies', 'current_medications', 'insurance_number'
        )

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'blood_type', 'emergency_contact_name', 'emergency_contact_phone',
            'medical_history', 'allergies', 'current_medications', 'insurance_number'
        )
