from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import update_session_auth_hash
from .models import User
from .serializers import (
    UserRegistrationSerializer, UserSerializer,
    UserProfileUpdateSerializer, ChangePasswordSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = UserProfileUpdateSerializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Profile updated successfully',
                'user': UserSerializer(self.get_object()).data
            }
        )

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        update_session_auth_hash(request, user)
        
        return Response({
            'message': 'Password changed successfully'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_stats(request):
    user = request.user
    stats = {}
    
    if user.user_type == 'patient':
        from appointments.models import Appointment
        stats = {
            'total_appointments': Appointment.objects.filter(patient__user=user).count(),
            'upcoming_appointments': Appointment.objects.filter(
                patient__user=user,
                status='scheduled'
            ).count(),
        }
    elif user.user_type == 'doctor':
        from appointments.models import Appointment
        stats = {
            'total_appointments': Appointment.objects.filter(doctor__user=user).count(),
            'today_appointments': Appointment.objects.filter(
                doctor__user=user,
                appointment_date__date=timezone.now().date()
            ).count(),
        }
    elif user.user_type in ['admin', 'super_admin']:
        stats = {
            'total_users': User.objects.count(),
            'total_patients': User.objects.filter(user_type='patient').count(),
            'total_doctors': User.objects.filter(user_type='doctor').count(),
        }
    
    return Response(stats)
