from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
from .models import Appointment
from .serializers import (
    AppointmentSerializer, AppointmentCreateSerializer, AppointmentUpdateSerializer
)

class AppointmentListView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'appointment_type', 'doctor', 'patient']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['-appointment_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        else:
            return Appointment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_appointment(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
        
        # Check permissions
        user = request.user
        if (user.user_type == 'patient' and appointment.patient.user != user) or \
           (user.user_type == 'doctor' and appointment.doctor.user != user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        appointment.status = 'cancelled'
        appointment.save()
        
        return Response({
            'message': 'Appointment cancelled successfully',
            'appointment': AppointmentSerializer(appointment).data
        })
    
    except Appointment.DoesNotExist:
        return Response(
            {'error': 'Appointment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upcoming_appointments(request):
    user = request.user
    now = timezone.now()
    
    if user.user_type == 'patient':
        appointments = Appointment.objects.filter(
            patient__user=user,
            appointment_date__gte=now,
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')[:5]
    elif user.user_type == 'doctor':
        appointments = Appointment.objects.filter(
            doctor__user=user,
            appointment_date__gte=now,
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')[:10]
    else:
        appointments = Appointment.objects.filter(
            appointment_date__gte=now,
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')[:20]
    
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
