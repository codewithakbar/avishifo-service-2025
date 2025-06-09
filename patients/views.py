from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Patient
from .serializers import PatientSerializer, PatientCreateSerializer, PatientUpdateSerializer

class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient':
            return Patient.objects.filter(user=user)
        elif user.user_type == 'doctor':
            # Doctors can see their patients
            from appointments.models import Appointment
            patient_ids = Appointment.objects.filter(
                doctor__user=user
            ).values_list('patient_id', flat=True).distinct()
            return Patient.objects.filter(id__in=patient_ids)
        else:
            # Admins can see all patients
            return Patient.objects.all()

class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PatientUpdateSerializer
        return PatientSerializer

class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def patient_medical_summary(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    # Check permissions
    user = request.user
    if user.user_type == 'patient' and patient.user != user:
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    from medical_records.models import MedicalRecord
    from appointments.models import Appointment
    
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')[:5]
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:5]
    
    summary = {
        'patient': PatientSerializer(patient).data,
        'recent_medical_records': [
            {
                'id': record.id,
                'diagnosis': record.diagnosis,
                'treatment': record.treatment,
                'date': record.created_at.date(),
                'doctor': record.doctor.user.full_name
            } for record in medical_records
        ],
        'recent_appointments': [
            {
                'id': appointment.id,
                'doctor': appointment.doctor.user.full_name,
                'date': appointment.appointment_date,
                'status': appointment.status,
                'notes': appointment.notes
            } for appointment in appointments
        ]
    }
    
    return Response(summary)
