# appointments/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from .models import Appointment
from .serializers import (
    AppointmentListSerializer,
    AppointmentDetailSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer,
)


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.select_related("patient", "doctor")

        if user.user_type == "doctor":
            queryset = queryset.filter(doctor=user)
        elif user.user_type == "patient":
            queryset = queryset.filter(patient=user)
        elif user.user_type in ["admin", "super_admin"]:
            # Admin can see all appointments
            pass
        else:
            queryset = queryset.none()

        # Filtering
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        priority_filter = self.request.query_params.get("priority")
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search)
                | Q(patient__last_name__icontains=search)
                | Q(reason__icontains=search)
                | Q(description__icontains=search)
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AppointmentListSerializer
        elif self.action == "create":
            return AppointmentCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return AppointmentUpdateSerializer
        return AppointmentDetailSerializer

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = "confirmed"
        appointment.confirmed_at = timezone.now()
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        appointment = self.get_object()
        rejection_reason = request.data.get("rejection_reason", "")

        appointment.status = "rejected"
        appointment.rejected_at = timezone.now()
        appointment.rejection_reason = rejection_reason
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        user = request.user
        queryset = self.get_queryset()

        stats = {
            "total": queryset.count(),
            "pending": queryset.filter(status="pending").count(),
            "confirmed": queryset.filter(status="confirmed").count(),
            "rejected": queryset.filter(status="rejected").count(),
            "high_priority": queryset.filter(priority="high").count(),
        }

        return Response(stats)
