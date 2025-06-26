from django.db.models import Count, Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Doctor, DoctorSchedule
from .serializers import (
    DoctorProfileSerializer,
    DoctorSerializer,
    DoctorCreateSerializer,
    DoctorUpdateSerializer,
    DoctorScheduleSerializer,
)
from django.utils import timezone  # Import timezone for date comparisons



class DoctorProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorProfileSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({"detail": "Profil topilmadi"}, status=404)

    def post(self, request):
        if hasattr(request.user, 'doctor_profile'):
            return Response({"detail": "Profil allaqachon mavjud"}, status=400)
        
        serializer = DoctorProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({"detail": "Profil topilmadi"}, status=404)

        serializer = DoctorProfileSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({"detail": "Profil topilmadi"}, status=404)

        serializer = DoctorProfileSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)




class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "specialty",
        "hospital",
        "is_available",
        "category",
        "degree",
        "online_consultation_available",  # New filter field
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "specialty",  # Existing
        "main_workplace",
        "medical_identifier",
        "languages_spoken",  # New search fields
        # To search by specialty/category/degree label, you'd need custom logic or a separate field
    ]
    ordering_fields = [
        "rating",
        "years_of_experience",
        "consultation_fee",  # Existing
        "patients_accepted_count",
        "consultations_count",
        "updated_at",  # New ordering fields
    ]
    ordering = ["-rating"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)
        if search_query:
            # Extend search to include specialty label if possible, or other text fields
            # For specialty label search, you might need to iterate through choices or use a more advanced search library
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
                | Q(specialty__icontains=search_query)  # Searches by code
                | Q(main_workplace__icontains=search_query)
                | Q(medical_identifier__icontains=search_query)
                | Q(
                    languages_spoken__icontains=search_query
                )  # Searches within JSONField as text
            )
        return queryset


class DoctorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return DoctorUpdateSerializer
        return DoctorSerializer


class DoctorProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )


class DoctorCreateView(generics.CreateAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Consider more restrictive permissions for doctor creation

    def perform_create(self, serializer):
        # Ensure the user creating the doctor profile is associated correctly
        # If the user is already authenticated and is the doctor, use request.user
        # If an admin is creating a doctor profile for another user, you'd need to handle user assignment
        serializer.save(
            user=self.request.user
        )  # Assuming the logged-in user is the doctor being created


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_dashboard_stats(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    # Check permissions
    user = request.user
    if user.user_type == "doctor" and doctor.user != user:
        return Response(
            {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    from appointments.models import Appointment  # Assuming Appointment model exists

    today = timezone.now().date()

    stats = {
        "total_appointments": Appointment.objects.filter(doctor=doctor).count(),
        "today_appointments": Appointment.objects.filter(
            doctor=doctor, appointment_date__date=today
        ).count(),
        "completed_appointments": Appointment.objects.filter(
            doctor=doctor, status="completed"
        ).count(),
        "pending_appointments": Appointment.objects.filter(
            doctor=doctor, status="scheduled"
        ).count(),
        "total_patients": Appointment.objects.filter(doctor=doctor)
        .values("patient")
        .distinct()
        .count(),
        # New stats from Doctor model
        "patients_accepted_count": doctor.patients_accepted_count,
        "consultations_count": doctor.consultations_count,
        "reviews_count": doctor.reviews_count,
    }

    return Response(stats)


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def doctor_schedule(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "GET":
        schedules = DoctorSchedule.objects.filter(doctor=doctor)
        serializer = DoctorScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # Check permissions
        if request.user != doctor.user and request.user.user_type not in [
            "admin",
            "super_admin",
        ]:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = DoctorScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(["GET"])
def doctor_specialties_list(request):
    """
    Returns a list of all available doctor specialties.
    """
    try:
        specialties = []
        for specialty_code, specialty_name in Doctor.SPECIALTIES:
            specialties.append({"value": specialty_code, "label": specialty_name})

        return JsonResponse(
            {"success": True, "data": specialties, "count": len(specialties)}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["GET"])
def doctor_specialties_with_stats(request):
    """
    Returns a list of specialties with the count of doctors in each.
    """
    try:
        specialty_stats = (
            Doctor.objects.values("specialty")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        stats_dict = {item["specialty"]: item["count"] for item in specialty_stats}

        specialties = []
        for specialty_code, specialty_name in Doctor.SPECIALTIES:
            specialties.append(
                {
                    "value": specialty_code,
                    "label": specialty_name,
                    "count": stats_dict.get(specialty_code, 0),
                }
            )

        return JsonResponse(
            {
                "success": True,
                "data": specialties,
                "total_specialties": len(specialties),
                "active_specialties": len([s for s in specialties if s["count"] > 0]),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# New views for DoctorSchedule (if not already defined in previous response)
# If you already have DoctorScheduleListView and DoctorScheduleDetailView, you can skip this.
class DoctorScheduleListView(generics.ListCreateAPIView):
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctor_pk = self.kwargs["doctor_pk"]
        doctor = get_object_or_404(Doctor, pk=doctor_pk)
        return DoctorSchedule.objects.filter(doctor=doctor)

    def perform_create(self, serializer):
        doctor_pk = self.kwargs["doctor_pk"]
        doctor = get_object_or_404(Doctor, pk=doctor_pk)
        # Check permissions for creating schedule
        if self.request.user != doctor.user and self.request.user.user_type not in [
            "admin",
            "super_admin",
        ]:
            raise permissions.PermissionDenied(
                "You do not have permission to create schedules for this doctor."
            )
        serializer.save(doctor=doctor)


class DoctorScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        # Check permissions for updating schedule
        doctor = serializer.instance.doctor
        if self.request.user != doctor.user and self.request.user.user_type not in [
            "admin",
            "super_admin",
        ]:
            raise permissions.PermissionDenied(
                "You do not have permission to update schedules for this doctor."
            )
        serializer.save()

    def perform_destroy(self, instance):
        # Check permissions for deleting schedule
        doctor = instance.doctor
        if self.request.user != doctor.user and self.request.user.user_type not in [
            "admin",
            "super_admin",
        ]:
            raise permissions.PermissionDenied(
                "You do not have permission to delete schedules for this doctor."
            )
        instance.delete()



class SpecialtyChoicesAPIView(APIView):
    def get(self, request):
        return Response(Doctor.SPECIALTIES)
    
    