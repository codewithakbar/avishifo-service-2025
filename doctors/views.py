from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Doctor, DoctorSchedule
from .serializers import (
    DoctorSerializer, DoctorCreateSerializer, DoctorUpdateSerializer,
    DoctorScheduleSerializer
)

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['specialty', 'hospital', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'specialty']
    ordering_fields = ['rating', 'years_of_experience', 'consultation_fee']
    ordering = ['-rating']

class DoctorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DoctorUpdateSerializer
        return DoctorSerializer

class DoctorCreateView(generics.CreateAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def doctor_dashboard_stats(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    # Check permissions
    user = request.user
    if user.user_type == 'doctor' and doctor.user != user:
        return Response(
            {'error': 'Permission denied'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    from appointments.models import Appointment
    from django.utils import timezone
    
    today = timezone.now().date()
    
    stats = {
        'total_appointments': Appointment.objects.filter(doctor=doctor).count(),
        'today_appointments': Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=today
        ).count(),
        'completed_appointments': Appointment.objects.filter(
            doctor=doctor,
            status='completed'
        ).count(),
        'pending_appointments': Appointment.objects.filter(
            doctor=doctor,
            status='scheduled'
        ).count(),
        'total_patients': Appointment.objects.filter(
            doctor=doctor
        ).values('patient').distinct().count(),
    }
    
    return Response(stats)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def doctor_schedule(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'GET':
        schedules = DoctorSchedule.objects.filter(doctor=doctor)
        serializer = DoctorScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Check permissions
        if request.user != doctor.user and request.user.user_type not in ['admin', 'super_admin']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = DoctorScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@require_http_methods(["GET"])
def doctor_specialties_list(request):
    """
    Возвращает список всех доступных специальностей врачей
    """
    try:
        # Получаем все специальности из модели Doctor
        specialties = []
        for specialty_code, specialty_name in Doctor.SPECIALTIES:
            specialties.append({
                'value': specialty_code,
                'label': specialty_name
            })
        
        return JsonResponse({
            'success': True,
            'data': specialties,
            'count': len(specialties)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)



@require_http_methods(["GET"])
def doctor_specialties_with_stats(request):
    """
    Возвращает список специальностей с количеством врачей в каждой
    """
    try:
        # Получаем статистику по специальностям
        specialty_stats = Doctor.objects.values('specialty').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Создаем словарь для быстрого поиска
        stats_dict = {item['specialty']: item['count'] for item in specialty_stats}
        
        # Формируем полный список специальностей
        specialties = []
        for specialty_code, specialty_name in Doctor.SPECIALTIES:
            specialties.append({
                'value': specialty_code,
                'label': specialty_name,
                'count': stats_dict.get(specialty_code, 0)
            })
        
        return JsonResponse({
            'success': True,
            'data': specialties,
            'total_specialties': len(specialties),
            'active_specialties': len([s for s in specialties if s['count'] > 0])
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


