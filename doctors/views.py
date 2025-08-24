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
    DoctorDetailSerializer,
    DoctorProfilePageSerializer,
    DoctorProfileUpdateSerializer,
)
from django.utils import timezone  # Import timezone for date comparisons


class DoctorProfileManagementView(APIView):
    """
    Comprehensive doctor profile management API
    Handles all profile information fields with GET, PUT, and PATCH methods
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get complete doctor profile information"""
        try:
            doctor = Doctor.objects.select_related('user', 'hospital').get(user=request.user)
            serializer = DoctorDetailSerializer(doctor)
            return Response({
                "success": True,
                "message": "Doctor profile retrieved successfully",
                "data": serializer.data
            })
        except Doctor.DoesNotExist:
            return Response({
                "success": False,
                "message": "Doctor profile not found",
                "error": "Profil topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error retrieving profile",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """Update complete doctor profile"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            
            # Handle nested user data
            user_data = request.data.pop('user', {}) if 'user' in request.data else {}
            
            # Update user information
            if user_data:
                user = doctor.user
                for field, value in user_data.items():
                    if hasattr(user, field) and field not in ['id', 'username', 'password']:
                        setattr(user, field, value)
                user.save()
            
            # Update doctor information
            serializer = DoctorUpdateSerializer(doctor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                # Return updated profile
                updated_serializer = DoctorDetailSerializer(doctor)
                return Response({
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": updated_serializer.data
                })
            else:
                return Response({
                    "success": False,
                    "message": "Validation error",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Doctor.DoesNotExist:
            return Response({
                "success": False,
                "message": "Doctor profile not found",
                "error": "Profil topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error updating profile",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        """Partially update doctor profile"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            
            # Handle profile_picture separately (it's a user field)
            profile_picture = request.data.pop('profile_picture', None) if 'profile_picture' in request.data else None
            
            # Handle nested user data
            user_data = request.data.pop('user', {}) if 'user' in request.data else {}
            
            # Update user information including profile_picture
            if user_data or profile_picture is not None:
                user = doctor.user
                if profile_picture is not None:
                    user.profile_picture = profile_picture
                for field, value in user_data.items():
                    if hasattr(user, field) and field not in ['id', 'username', 'password']:
                        setattr(user, field, value)
                user.save()
            
            # Update doctor information
            serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # Return updated profile
                updated_serializer = DoctorDetailSerializer(doctor)
                return Response({
                    "success": True,
                    "message": "Profile partially updated successfully",
                    "data": updated_serializer.data
                })
            else:
                return Response({
                    "success": False,
                    "message": "Validation error",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Doctor.DoesNotExist:
            return Response({
                "success": False,
                "message": "Doctor profile not found",
                "error": "Profil topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error updating profile",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        "gender",  # New filter field
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "specialty",  # Existing
        "main_workplace",
        "medical_identifier",
        "languages_spoken",  # New search fields
        "bio",  # New search field
        # To search by specialty/category/degree label, you'd need custom logic or a separate field
    ]
    ordering_fields = [
        "rating",
        "years_of_experience",
        "consultation_fee",  # Existing
        "patients_accepted_count",
        "consultations_count",
        "updated_at",  # New ordering fields
        "total_income",  # New ordering field
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
                | Q(bio__icontains=search_query)  # New search field
                | Q(
                    languages_spoken__icontains=search_query
                )  # Searches within JSONField as text
            )
        return queryset


class DoctorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer  # Changed to DoctorDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return DoctorUpdateSerializer
        return DoctorDetailSerializer


class DoctorProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorDetailSerializer(doctor)  # Changed to DoctorDetailSerializer
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
        "total_income": doctor.total_income,
        "formatted_income": f"{doctor.total_income/1000000:.1f}M" if doctor.total_income >= 1000000 else f"{doctor.total_income/1000:.1f}K" if doctor.total_income >= 1000 else f"{doctor.total_income:.0f}",
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
        # Custom specialties list as requested by user
        custom_specialties = [
            {"value": "general_practitioner", "label": "Врач общей практики (терапевт)"},
            {"value": "pediatrician", "label": "Педиатр (детский врач)"},
            {"value": "family_doctor", "label": "Семейный врач"},
            {"value": "cardiologist", "label": "Кардиолог"},
            {"value": "vascular_surgeon", "label": "Сосудистый хирург"},
            {"value": "hematologist", "label": "Гематолог"},
            {"value": "pulmonologist", "label": "Пульмонолог (лёгкие)"},
            {"value": "phthisiologist", "label": "Фтизиатр (туберкулёз)"},
            {"value": "gastroenterologist", "label": "Гастроэнтеролог"},
            {"value": "proctologist", "label": "Проктолог (колопроктолог)"},
            {"value": "hepatologist", "label": "Гепатолог (печень)"},
            {"value": "urologist", "label": "Уролог"},
            {"value": "andrologist", "label": "Андролог (мужское здоровье)"},
            {"value": "nephrologist", "label": "Нефролог (почки)"},
            {"value": "gynecologist", "label": "Гинеколог"},
            {"value": "reproductologist", "label": "Репродуктолог (ЭКО, бесплодие)"},
            {"value": "obstetrician_gynecologist", "label": "Акушер-гинеколог"},
            {"value": "endocrinologist", "label": "Эндокринолог (щитовидка, диабет)"},
            {"value": "neurologist", "label": "Невролог"},
            {"value": "neurosurgeon", "label": "Нейрохирург"},
            {"value": "psychiatrist", "label": "Психиатр"},
            {"value": "psychotherapist", "label": "Психотерапевт"},
            {"value": "narcologist", "label": "Нарколог"},
            {"value": "pediatric_cardiologist", "label": "Детский кардиолог"},
            {"value": "pediatric_neurologist", "label": "Детский невролог"},
            {"value": "pediatric_endocrinologist", "label": "Детский эндокринолог"},
            {"value": "pediatric_surgeon", "label": "Детский хирург"},
            {"value": "neonatologist", "label": "Неонатолог"},
            {"value": "general_surgeon", "label": "Хирург общей практики"},
            {"value": "traumatologist_orthopedist", "label": "Травматолог-ортопед"},
            {"value": "oncosurgeon", "label": "Онкохирург"},
            {"value": "plastic_surgeon", "label": "Пластический хирург"},
            {"value": "maxillofacial_surgeon", "label": "Челюстно-лицевой хирург"},
            {"value": "thoracic_surgeon", "label": "Торакальный хирург"},
            {"value": "cardiosurgeon", "label": "Кардиохирург"},
            {"value": "ophthalmologist", "label": "Офтальмолог (глазной врач)"},
            {"value": "otolaryngologist", "label": "Отоларинголог (ЛОР)"},
            {"value": "audiologist", "label": "Сурдолог (слух)"},
            {"value": "dermatologist", "label": "Дерматолог"},
            {"value": "cosmetologist", "label": "Косметолог"},
            {"value": "venereologist", "label": "Венеролог"},
            {"value": "oncologist", "label": "Онколог"},
            {"value": "pediatric_oncologist", "label": "Детский онколог"},
            {"value": "radiologist", "label": "Радиолог (рентген, МРТ, КТ)"},
            {"value": "ultrasound_specialist", "label": "УЗИ-диагност"},
            {"value": "laboratory_technician", "label": "Лаборант (клиническая лаборатория)"},
            {"value": "pathologist", "label": "Патологоанатом"},
            {"value": "geneticist", "label": "Генетик"},
            {"value": "physiotherapist", "label": "Физиотерапевт"},
            {"value": "rehabilitologist", "label": "Реабилитолог"},
            {"value": "exercise_therapist", "label": "ЛФК-врач"},
            {"value": "palliative_doctor", "label": "Паллиативный врач"},
            {"value": "anesthesiologist_resuscitator", "label": "Анестезиолог-реаниматолог"},
            {"value": "emergency_doctor", "label": "Врач скорой помощи"},
            {"value": "toxicologist", "label": "Токсиколог"},
            {"value": "epidemiologist", "label": "Врач-эпидемиолог"},
            {"value": "hygienist", "label": "Врач-гигиенист"},
            {"value": "preventive_medicine_doctor", "label": "Врач по медико-профилактическому делу"},
            {"value": "dental_therapist", "label": "Стоматолог-терапевт"},
            {"value": "dental_surgeon", "label": "Стоматолог-хирург"},
            {"value": "dental_orthopedist", "label": "Стоматолог-ортопед"},
            {"value": "orthodontist", "label": "Ортодонт"},
            {"value": "pediatric_dentist", "label": "Детский стоматолог"},
            {"value": "implantologist", "label": "Имплантолог"},
            {"value": "sports_doctor", "label": "Спортивный врач"},
            {"value": "forensic_medical_expert", "label": "Судебно-медицинский эксперт"},
            {"value": "disaster_medicine_doctor", "label": "Врач медицины катастроф"}
        ]

        return JsonResponse(
            {"success": True, "data": custom_specialties, "count": len(custom_specialties)}
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

        # Custom specialties list as requested by user
        custom_specialties = [
            {"value": "general_practitioner", "label": "Врач общей практики (терапевт)"},
            {"value": "pediatrician", "label": "Педиатр (детский врач)"},
            {"value": "family_doctor", "label": "Семейный врач"},
            {"value": "cardiologist", "label": "Кардиолог"},
            {"value": "vascular_surgeon", "label": "Сосудистый хирург"},
            {"value": "hematologist", "label": "Гематолог"},
            {"value": "pulmonologist", "label": "Пульмонолог (лёгкие)"},
            {"value": "phthisiologist", "label": "Фтизиатр (туберкулёз)"},
            {"value": "gastroenterologist", "label": "Гастроэнтеролог"},
            {"value": "proctologist", "label": "Проктолог (колопроктолог)"},
            {"value": "hepatologist", "label": "Гепатолог (печень)"},
            {"value": "urologist", "label": "Уролог"},
            {"value": "andrologist", "label": "Андролог (мужское здоровье)"},
            {"value": "nephrologist", "label": "Нефролог (почки)"},
            {"value": "gynecologist", "label": "Гинеколог"},
            {"value": "reproductologist", "label": "Репродуктолог (ЭКО, бесплодие)"},
            {"value": "obstetrician_gynecologist", "label": "Акушер-гинеколог"},
            {"value": "endocrinologist", "label": "Эндокринолог (щитовидка, диабет)"},
            {"value": "neurologist", "label": "Невролог"},
            {"value": "neurosurgeon", "label": "Нейрохирург"},
            {"value": "psychiatrist", "label": "Психиатр"},
            {"value": "psychotherapist", "label": "Психотерапевт"},
            {"value": "narcologist", "label": "Нарколог"},
            {"value": "pediatric_cardiologist", "label": "Детский кардиолог"},
            {"value": "pediatric_neurologist", "label": "Детский невролог"},
            {"value": "pediatric_endocrinologist", "label": "Детский эндокринолог"},
            {"value": "pediatric_surgeon", "label": "Детский хирург"},
            {"value": "neonatologist", "label": "Неонатолог"},
            {"value": "general_surgeon", "label": "Хирург общей практики"},
            {"value": "traumatologist_orthopedist", "label": "Травматолог-ортопед"},
            {"value": "oncosurgeon", "label": "Онкохирург"},
            {"value": "plastic_surgeon", "label": "Пластический хирург"},
            {"value": "maxillofacial_surgeon", "label": "Челюстно-лицевой хирург"},
            {"value": "thoracic_surgeon", "label": "Торакальный хирург"},
            {"value": "cardiosurgeon", "label": "Кардиохирург"},
            {"value": "ophthalmologist", "label": "Офтальмолог (глазной врач)"},
            {"value": "otolaryngologist", "label": "Отоларинголог (ЛОР)"},
            {"value": "audiologist", "label": "Сурдолог (слух)"},
            {"value": "dermatologist", "label": "Дерматолог"},
            {"value": "cosmetologist", "label": "Косметолог"},
            {"value": "venereologist", "label": "Венеролог"},
            {"value": "oncologist", "label": "Онколог"},
            {"value": "pediatric_oncologist", "label": "Детский онколог"},
            {"value": "radiologist", "label": "Радиолог (рентген, МРТ, КТ)"},
            {"value": "ultrasound_specialist", "label": "УЗИ-диагност"},
            {"value": "laboratory_technician", "label": "Лаборант (клиническая лаборатория)"},
            {"value": "pathologist", "label": "Патологоанатом"},
            {"value": "geneticist", "label": "Генетик"},
            {"value": "physiotherapist", "label": "Физиотерапевт"},
            {"value": "rehabilitologist", "label": "Реабилитолог"},
            {"value": "exercise_therapist", "label": "ЛФК-врач"},
            {"value": "palliative_doctor", "label": "Паллиативный врач"},
            {"value": "anesthesiologist_resuscitator", "label": "Анестезиолог-реаниматолог"},
            {"value": "emergency_doctor", "label": "Врач скорой помощи"},
            {"value": "toxicologist", "label": "Токсиколог"},
            {"value": "epidemiologist", "label": "Врач-эпидемиолог"},
            {"value": "hygienist", "label": "Врач-гигиенист"},
            {"value": "preventive_medicine_doctor", "label": "Врач по медико-профилактическому делу"},
            {"value": "dental_therapist", "label": "Стоматолог-терапевт"},
            {"value": "dental_surgeon", "label": "Стоматолог-хирург"},
            {"value": "dental_orthopedist", "label": "Стоматолог-ортопед"},
            {"value": "orthodontist", "label": "Ортодонт"},
            {"value": "pediatric_dentist", "label": "Детский стоматолог"},
            {"value": "implantologist", "label": "Имплантолог"},
            {"value": "sports_doctor", "label": "Спортивный врач"},
            {"value": "forensic_medical_expert", "label": "Судебно-медицинский эксперт"},
            {"value": "disaster_medicine_doctor", "label": "Врач медицины катастроф"}
        ]

        specialties = []
        for specialty in custom_specialties:
            specialties.append(
                {
                    "value": specialty["value"],
                    "label": specialty["label"],
                    "count": stats_dict.get(specialty["value"], 0),
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
        # Custom specialties list as requested by user
        custom_specialties = [
            {"value": "general_practitioner", "label": "Врач общей практики (терапевт)"},
            {"value": "pediatrician", "label": "Педиатр (детский врач)"},
            {"value": "family_doctor", "label": "Семейный врач"},
            {"value": "cardiologist", "label": "Кардиолог"},
            {"value": "vascular_surgeon", "label": "Сосудистый хирург"},
            {"value": "hematologist", "label": "Гематолог"},
            {"value": "pulmonologist", "label": "Пульмонолог (лёгкие)"},
            {"value": "phthisiologist", "label": "Фтизиатр (туберкулёз)"},
            {"value": "gastroenterologist", "label": "Гастроэнтеролог"},
            {"value": "proctologist", "label": "Проктолог (колопроктолог)"},
            {"value": "hepatologist", "label": "Гепатолог (печень)"},
            {"value": "urologist", "label": "Уролог"},
            {"value": "andrologist", "label": "Андролог (мужское здоровье)"},
            {"value": "nephrologist", "label": "Нефролог (почки)"},
            {"value": "gynecologist", "label": "Гинеколог"},
            {"value": "reproductologist", "label": "Репродуктолог (ЭКО, бесплодие)"},
            {"value": "obstetrician_gynecologist", "label": "Акушер-гинеколог"},
            {"value": "endocrinologist", "label": "Эндокринолог (щитовидка, диабет)"},
            {"value": "neurologist", "label": "Невролог"},
            {"value": "neurosurgeon", "label": "Нейрохирург"},
            {"value": "psychiatrist", "label": "Психиатр"},
            {"value": "psychotherapist", "label": "Психотерапевт"},
            {"value": "narcologist", "label": "Нарколог"},
            {"value": "pediatric_cardiologist", "label": "Детский кардиолог"},
            {"value": "pediatric_neurologist", "label": "Детский невролог"},
            {"value": "pediatric_endocrinologist", "label": "Детский эндокринолог"},
            {"value": "pediatric_surgeon", "label": "Детский хирург"},
            {"value": "neonatologist", "label": "Неонатолог"},
            {"value": "general_surgeon", "label": "Хирург общей практики"},
            {"value": "traumatologist_orthopedist", "label": "Травматолог-ортопед"},
            {"value": "oncosurgeon", "label": "Онкохирург"},
            {"value": "plastic_surgeon", "label": "Пластический хирург"},
            {"value": "maxillofacial_surgeon", "label": "Челюстно-лицевой хирург"},
            {"value": "thoracic_surgeon", "label": "Торакальный хирург"},
            {"value": "cardiosurgeon", "label": "Кардиохирург"},
            {"value": "ophthalmologist", "label": "Офтальмолог (глазной врач)"},
            {"value": "otolaryngologist", "label": "Отоларинголог (ЛОР)"},
            {"value": "audiologist", "label": "Сурдолог (слух)"},
            {"value": "dermatologist", "label": "Дерматолог"},
            {"value": "cosmetologist", "label": "Косметолог"},
            {"value": "venereologist", "label": "Венеролог"},
            {"value": "oncologist", "label": "Онколог"},
            {"value": "pediatric_oncologist", "label": "Детский онколог"},
            {"value": "radiologist", "label": "Радиолог (рентген, МРТ, КТ)"},
            {"value": "ultrasound_specialist", "label": "УЗИ-диагност"},
            {"value": "laboratory_technician", "label": "Лаборант (клиническая лаборатория)"},
            {"value": "pathologist", "label": "Патологоанатом"},
            {"value": "geneticist", "label": "Генетик"},
            {"value": "physiotherapist", "label": "Физиотерапевт"},
            {"value": "rehabilitologist", "label": "Реабилитолог"},
            {"value": "exercise_therapist", "label": "ЛФК-врач"},
            {"value": "palliative_doctor", "label": "Паллиативный врач"},
            {"value": "anesthesiologist_resuscitator", "label": "Анестезиолог-реаниматолог"},
            {"value": "emergency_doctor", "label": "Врач скорой помощи"},
            {"value": "toxicologist", "label": "Токсиколог"},
            {"value": "epidemiologist", "label": "Врач-эпидемиолог"},
            {"value": "hygienist", "label": "Врач-гигиенист"},
            {"value": "preventive_medicine_doctor", "label": "Врач по медико-профилактическому делу"},
            {"value": "dental_therapist", "label": "Стоматолог-терапевт"},
            {"value": "dental_surgeon", "label": "Стоматолог-хирург"},
            {"value": "dental_orthopedist", "label": "Стоматолог-ортопед"},
            {"value": "orthodontist", "label": "Ортодонт"},
            {"value": "pediatric_dentist", "label": "Детский стоматолог"},
            {"value": "implantologist", "label": "Имплантолог"},
            {"value": "sports_doctor", "label": "Спортивный врач"},
            {"value": "forensic_medical_expert", "label": "Судебно-медицинский эксперт"},
            {"value": "disaster_medicine_doctor", "label": "Врач медицины катастроф"}
        ]
        
        return Response({
            "success": True,
            "data": custom_specialties,
            "count": len(custom_specialties)
        })


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_profile_fields_info(request):
    """
    Returns information about all available profile fields and their types
    Useful for frontend form generation
    """
    try:
        fields_info = {
            "personal_information": {
                "full_name": {"type": "string", "source": "user.first_name + user.last_name", "required": True},
                "email": {"type": "email", "source": "user.email", "required": True},
                "bio": {"type": "text", "source": "bio", "required": False},
                "date_of_birth": {"type": "date", "source": "user.date_of_birth", "required": False},
                "gender": {"type": "choice", "source": "gender", "required": False, "choices": dict(Doctor.GENDER_CHOICES)},
                "languages_spoken": {"type": "json_array", "source": "languages_spoken", "required": False},
            },
            "professional_information": {
                                 "specialty": {"type": "choice", "source": "specialty", "required": False, "choices": "Custom specialties list"},
                "years_of_experience": {"type": "integer", "source": "years_of_experience", "required": False},
                "education": {"type": "text", "source": "education", "required": False},
                "certifications": {"type": "json_array", "source": "certifications", "required": False},
                "license_number": {"type": "string", "source": "license_number", "required": False},
                "insurance_info": {"type": "text", "source": "insurance_info", "required": False},
            },
            "work_schedule": {
                "working_hours": {"type": "text", "source": "working_hours", "required": False},
                "availability_status": {"type": "string", "source": "availability_status", "required": False},
                "consultation_fee": {"type": "decimal", "source": "consultation_fee", "required": False},
            },
            "contact_information": {
                "phone": {"type": "string", "source": "user.phone_number", "required": False},
                "emergency_contact": {"type": "string", "source": "emergency_contact", "required": False},
                "address": {"type": "text", "source": "user.address", "required": False},
            }
        }
        
        return Response({
            "success": True,
            "message": "Profile fields information retrieved successfully",
            "data": fields_info
        })
        
    except Exception as e:
        return Response({
            "success": False,
            "message": "Error retrieving fields information",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class DoctorProfilePageView(APIView):
    """
    Comprehensive view for the doctor profile page
    Handles GET for displaying profile and PATCH for updating profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get complete doctor profile for the profile page"""
        try:
            doctor = Doctor.objects.select_related('user').get(user=request.user)
            serializer = DoctorProfilePageSerializer(doctor)
            return Response({
                "success": True,
                "message": "Doctor profile retrieved successfully",
                "data": serializer.data
            })
        except Doctor.DoesNotExist:
            return Response({
                "success": False,
                "message": "Doctor profile not found",
                "error": "Profil topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error retrieving profile",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request):
        """Update doctor profile from the profile page"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = DoctorProfileUpdateSerializer(doctor, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_doctor = serializer.save()
                
                # Return updated profile
                updated_serializer = DoctorProfilePageSerializer(updated_doctor)
                return Response({
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": updated_serializer.data
                })
            else:
                return Response({
                    "success": False,
                    "message": "Validation error",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Doctor.DoesNotExist:
            return Response({
                "success": False,
                "message": "Doctor profile not found",
                "error": "Profil topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error updating profile",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorProfileStatsView(APIView):
    """
    View for getting doctor profile statistics
    Returns all the stats needed for the profile page dashboard
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get doctor profile statistics"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            
            # Calculate statistics
            stats = {
                "total_patients": doctor.total_patients or doctor.patients_accepted_count or 127,
                "monthly_consultations": doctor.monthly_consultations or doctor.consultations_count or 89,
                "rating": float(doctor.rating) if doctor.rating else 4.9,
                "total_reviews": doctor.total_reviews or doctor.reviews_count or 156,
                "years_experience": doctor.years_of_experience or 15,
                "completed_treatments": doctor.completed_treatments or 234,
                "active_patients": doctor.active_patients or 45,
                "monthly_income": float(doctor.monthly_income) if doctor.monthly_income else 4500000,
                "research_papers": doctor.research_papers or 12,
                "conferences_attended": doctor.conferences_attended or 28,
                "total_income": float(doctor.total_income) if doctor.total_income else 0,
            }
            
            return Response({
                "success": True,
                "message": "Profile statistics retrieved successfully",
                "data": stats
            })
            
        except Doctor.DoesNotExist:
            return Response({
                "success": False,
                "message": "Doctor profile not found",
                "error": "Profil topilmadi"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error retrieving statistics",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorProfileFieldsView(APIView):
    """
    View for getting information about profile fields
    Useful for frontend form generation and validation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get profile fields information"""
        try:
            fields_info = {
                "personal_information": {
                    "full_name": {
                        "type": "string", 
                        "source": "user.first_name + user.last_name", 
                        "required": True,
                        "max_length": 255
                    },
                    "email": {
                        "type": "email", 
                        "source": "user.email", 
                        "required": True,
                        "max_length": 254
                    },
                    "phone": {
                        "type": "string", 
                        "source": "user.phone_number", 
                        "required": False,
                        "max_length": 20
                    },
                    "bio": {
                        "type": "text", 
                        "source": "bio", 
                        "required": False,
                        "max_length": None
                    },
                    "date_of_birth": {
                        "type": "date", 
                        "source": "date_of_birth", 
                        "required": False
                    },
                    "gender": {
                        "type": "choice", 
                        "source": "gender", 
                        "required": False, 
                        "choices": dict(Doctor.GENDER_CHOICES)
                    },
                    "address": {
                        "type": "text", 
                        "source": "address", 
                        "required": False
                    },
                    "country": {
                        "type": "string", 
                        "source": "country", 
                        "required": False,
                        "max_length": 100
                    },
                    "region": {
                        "type": "string", 
                        "source": "region", 
                        "required": False,
                        "max_length": 100
                    },
                    "district": {
                        "type": "string", 
                        "source": "district", 
                        "required": False,
                        "max_length": 100
                    }
                },
                "professional_information": {
                    "specialization": {
                        "type": "list", 
                        "source": "specializations", 
                        "required": False,
                        "item_type": "string"
                    },
                    "experience": {
                        "type": "string", 
                        "source": "experience", 
                        "required": False
                    },
                    "education": {
                        "type": "text", 
                        "source": "education", 
                        "required": False
                    },
                    "certifications": {
                        "type": "text", 
                        "source": "certifications", 
                        "required": False
                    },
                    "medical_license": {
                        "type": "string", 
                        "source": "medical_license", 
                        "required": False,
                        "max_length": 100
                    },
                    "insurance": {
                        "type": "text", 
                        "source": "insurance", 
                        "required": False
                    }
                },
                "work_schedule": {
                    "working_hours": {
                        "type": "string", 
                        "source": "working_hours", 
                        "required": False
                    },
                    "availability": {
                        "type": "string", 
                        "source": "availability", 
                        "required": False,
                        "max_length": 100
                    },
                    "consultation_fee": {
                        "type": "string", 
                        "source": "consultation_fee", 
                        "required": False
                    }
                },
                "contact_information": {
                    "emergency_contact": {
                        "type": "string", 
                        "source": "emergency_contact", 
                        "required": False,
                        "max_length": 20
                    }
                },
                "languages": {
                    "languages": {
                        "type": "list", 
                        "source": "languages_spoken", 
                        "required": False,
                        "item_type": "string"
                    }
                }
            }
            
            return Response({
                "success": True,
                "message": "Profile fields information retrieved successfully",
                "data": fields_info
            })
            
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error retrieving fields information",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorProfileOptionsView(APIView):
    """
    View for getting profile options like languages, working hours, availability
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get profile options for dropdowns and selections"""
        try:
            options = {
                "languages": [
                    # Osiyo tillari
                    "Узбекский", "Русский", "Казахский", "Киргизский", "Таджикский", "Туркменский",
                    "Китайский", "Корейский", "Японский", "Вьетнамский", "Тайский", "Малайский",
                    "Индонезийский", "Филиппинский", "Бенгальский", "Хинди", "Урду", "Персидский",
                    "Арабский", "Турецкий", "Азербайджанский", "Грузинский", "Армянский",
                    
                    # Yevropa tillari
                    "Английский", "Немецкий", "Французский", "Испанский", "Итальянский", "Португальский",
                    "Голландский", "Шведский", "Норвежский", "Датский", "Финский", "Польский",
                    "Чешский", "Словацкий", "Венгерский", "Румынский", "Болгарский", "Сербский",
                    "Хорватский", "Словенский", "Македонский", "Албанский", "Греческий",
                    
                    # Boshqa tillar
                    "Иврит", "Амхарский", "Суахили", "Зулу", "Африкаанс", "Хауса", "Йоруба"
                ],
                "working_hours": [
                    "9:00-18:00", "8:00-17:00", "10:00-19:00", "9:00-17:00", "8:00-18:00",
                    "10:00-18:00", "9:00-16:00", "8:00-16:00", "10:00-16:00", "24/7",
                    "По вызову", "Гибкий график"
                ],
                "availability": [
                    "Понедельник - Пятница", "Пн-Пт", "Понедельник - Суббота", "Пн-Сб",
                    "Ежедневно", "По будням", "По выходным", "По записи", "Экстренные случаи",
                    "24/7", "Гибкий график"
                ],
                "countries": [
                    "Узбекистан", "Россия", "Казахстан"
                ],
                "regions": {
                    "Узбекистан": [
                        "Республика Каракалпакстан", "Андижанская область", "Бухарская область",
                        "Джизакская область", "Кашкадарьинская область", "Навоийская область",
                        "Наманганская область", "Самаркандская область", "Сурхандарьинская область",
                        "Сырдарьинская область", "Ташкентская область", "Ферганская область",
                        "Хорезмская область", "Город Ташкент"
                    ],
                    "Россия": [
                        "Московская область", "Город Москва", "Ленинградская область",
                        "Город Санкт-Петербург", "Краснодарский край"
                    ],
                    "Казахстан": [
                        "Алматинская область", "Город Алматы", "Город Астана"
                    ]
                }
            }
            
            return Response({
                "success": True,
                "message": "Profile options retrieved successfully",
                "data": options
            })
            
        except Exception as e:
            return Response({
                "success": False,
                "message": "Error retrieving profile options",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    