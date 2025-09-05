from rest_framework import generics, permissions, status, serializers, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.utils import timezone

from patients.permissions import IsDoctorUser

from .models import (
    KasallikTarixi,
    MedicalHistoryItem,
    MedicalRecord,
    Patient,
    PatientDocument,
    PatientVaqtincha,
    PrescribedMedication,
    VitalSign,
)
from .serializers import (
    KasallikTarixiSerializer,
    MedicalHistoryItemCreateSerializer,
    MedicalHistoryItemSerializer,
    MedicalRecordSerializer,
    PatientDocumentCreateSerializer,
    PatientDocumentSerializer,
    PatientSerializer,
    PatientCreateSerializer,
    PatientUpdateSerializer,
    PatientVaqtinchaSerializer,
    PrescribedMedicationCreateSerializer,
    PrescribedMedicationSerializer,
    VitalSignCreateSerializer,
    VitalSignSerializer,
)


class KasallikTarixiAPIView(APIView):
    permission_classes = [IsDoctorUser]

    def get(self, request, pk=None):
        if pk is not None:
            instance = get_object_or_404(KasallikTarixi, pk=pk)
            serializer = KasallikTarixiSerializer(instance)
            return Response(serializer.data)

        patient_id = request.query_params.get("patient_id")
        if patient_id:
            queryset = KasallikTarixi.objects.filter(patient_id=patient_id).order_by('-yuborilgan_vaqt')
        else:
            queryset = KasallikTarixi.objects.all().order_by('-yuborilgan_vaqt')

        serializer = KasallikTarixiSerializer(queryset, many=True)
        return Response(serializer.data)

        
    def post(self, request, *args, **kwargs):
        serializer = KasallikTarixiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ma'lumotlar saqlandi."}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        instance = get_object_or_404(KasallikTarixi, pk=pk)
        serializer = KasallikTarixiSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ma'lumotlar to‘liq yangilandi."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        instance = get_object_or_404(KasallikTarixi, pk=pk)
        serializer = KasallikTarixiSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ma'lumotlar qisman yangilandi."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientListAPIView(ListAPIView):
    serializer_class = PatientVaqtinchaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = PatientVaqtincha.objects.all()

        # faqat doctorlar kirish huquqiga ega
        if user.user_type != 'doctor':
            return PatientVaqtincha.objects.none()

        # query params orqali passport qidiruvi
        passport_series = self.request.query_params.get('passport_series')
        passport_number = self.request.query_params.get('passport_number')

        if passport_series and passport_number:
            # Har qanday doctor passport orqali ko'rishi mumkin
            return queryset.filter(passport_series=passport_series, passport_number=passport_number)
        
        # Aks holda faqat o'zi yaratganlarini ko'rsat
        return queryset.filter(created_by=user)


class PatientRetrieveAPIView(RetrieveAPIView):
    queryset = PatientVaqtincha.objects.all()
    serializer_class = PatientVaqtinchaSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"  # or use 'pk' if preferred


class PatientUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, id):
        try:
            # Convert string ID to integer for database lookup
            patient_id = int(id)
            patient = PatientVaqtincha.objects.get(id=patient_id)
            
            # Check if user has permission to update this patient
            # For now, allow all authenticated users to update patients
            # if patient.created_by != request.user and not request.user.is_staff:
            #     return Response(
            #         {"error": "You don't have permission to update this patient"},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            
            serializer = PatientVaqtinchaSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Patient updated successfully",
                    "data": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except PatientVaqtincha.DoesNotExist:
            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, id):
        try:
            # Convert string ID to integer for database lookup
            patient_id = int(id)
            patient = PatientVaqtincha.objects.get(id=patient_id)
            
            # Check if user has permission to delete this patient
            # For now, allow all authenticated users to delete patients
            # if patient.created_by != request.user and not request.user.is_staff:
            #     return Response(
            #         {"error": "You don't have permission to delete this patient"},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            
            # Soft delete - update status to deleted
            patient.status = 'deleted'
            patient.deleted_at = timezone.now()
            patient.save()
            
            return Response({
                "message": "Patient deleted successfully"
            })
            
        except PatientVaqtincha.DoesNotExist:
            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientArchiveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, id):
        try:
            # Convert string ID to integer for database lookup
            patient_id = int(id)
            patient = PatientVaqtincha.objects.get(id=patient_id)
            
            # Check if user has permission to archive this patient
            # For now, allow all authenticated users to archive patients
            # if patient.created_by != request.user and not request.user.is_staff:
            #     return Response(
            #         {"error": "You don't have permission to archive this patient"},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            
            # Get status from request body, default to 'archived' if not provided
            new_status = request.data.get('status', 'archived')
            
            # Update status
            patient.status = new_status
            
            if new_status == 'archived':
                patient.archived_at = timezone.now()
                patient.deleted_at = None
            elif new_status == 'active':
                patient.archived_at = None
                patient.deleted_at = None
            elif new_status == 'deleted':
                patient.deleted_at = timezone.now()
                patient.archived_at = None
                
            patient.save()
            
            print(f"Patient {patient_id} status updated to: {patient.status}")
            
            serializer = PatientVaqtinchaSerializer(patient)
            return Response({
                "message": f"Patient status updated to {new_status} successfully",
                "data": serializer.data
            })
            
        except PatientVaqtincha.DoesNotExist:
            return Response(
                {"error": "Patient not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Faqat tizimga kirgan foydalanuvchilar uchun

    def post(self, request):
        # Ensure status is set to 'active' if not provided
        data = request.data.copy()
        if 'status' not in data:
            data['status'] = 'active'
            
        serializer = PatientVaqtinchaSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)  # created_by ni belgilaymiz
            return Response(
                {"message": "Пациент успешно создан", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == "patient":
            return Patient.objects.filter(user=user)
        elif user.user_type == "doctor":
            # Doctors can see their patients
            from appointments.models import Appointment

            patient_ids = (
                Appointment.objects.filter(doctor__user=user)
                .values_list("patient_id", flat=True)
                .distinct()
            )
            return Patient.objects.filter(id__in=patient_ids)
        else:
            # Admins can see all patients
            return Patient.objects.all()


class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PatientUpdateSerializer
        return PatientSerializer


class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def patient_medical_summary(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    # Check permissions
    user = request.user
    if user.user_type == "patient" and patient.user != user:
        return Response(
            {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )

    from medical_records.models import MedicalRecord
    from appointments.models import Appointment

    medical_records = MedicalRecord.objects.filter(patient=patient).order_by(
        "-created_at"
    )[:5]
    appointments = Appointment.objects.filter(patient=patient).order_by(
        "-appointment_date"
    )[:5]

    summary = {
        "patient": PatientSerializer(patient).data,
        "recent_medical_records": [
            {
                "id": record.id,
                "diagnosis": record.diagnosis,
                "treatment": record.treatment,
                "date": record.created_at.date(),
                "doctor": record.doctor.user.full_name,
            }
            for record in medical_records
        ],
        "recent_appointments": [
            {
                "id": appointment.id,
                "doctor": appointment.doctor.user.full_name,
                "date": appointment.appointment_date,
                "status": appointment.status,
                "notes": appointment.notes,
            }
            for appointment in appointments
        ],
    }

    return Response(summary)


def is_doctor(user):
    return user.is_authenticated and user.user_type == "doctor"


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Замените на более строгие пермишены

    def get_queryset(self):
        user = self.request.user
        if is_doctor(user):
            # Доктор может видеть всех пациентов (или только тех, с кем он связан - нужна доп. логика)
            return Patient.objects.all()
        elif user.is_authenticated and hasattr(user, "patient_profile"):
            # Пациент видит только свой профиль
            return Patient.objects.filter(user=user)
        return Patient.objects.none()

    # def perform_create(self, serializer):
    #     # Логика для создания пациента, возможно, привязка к текущему пользователю, если он не пациент еще
    #     serializer.save()


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = (
        MedicalRecord.objects.select_related("patient__user", "doctor")
        .prefetch_related("history_items", "prescriptions", "vital_signs", "documents")
        .all()
    )
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]  # Замените

    def get_queryset(self):
        user = self.request.user
        if is_doctor(user):
            # Доктор видит медкарты, где он автор, или все, если админ (нужна доп. логика)
            return MedicalRecord.objects.filter(doctor=user)
        elif user.is_authenticated and hasattr(user, "patient_profile"):
            # Пациент видит только свои медкарты
            return MedicalRecord.objects.filter(patient=user.patient_profile)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        if not is_doctor(self.request.user):
            raise serializers.ValidationError(
                "Только доктор может создавать медицинские записи."
            )
        serializer.save(doctor=self.request.user)


# ViewSets для отдельных элементов медицинской карты
# Это позволяет добавлять элементы к существующей медкарте


class MedicalHistoryItemViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistoryItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return MedicalHistoryItemCreateSerializer
        return MedicalHistoryItemSerializer

    def get_queryset(self):
        # Фильтрация по правам доступа (например, только для записей, к которым у доктора есть доступ)
        # или по medical_record_id из URL, если используется вложенный роутинг
        return MedicalHistoryItem.objects.all()  # Заменить на фильтрованный queryset

    # def perform_create(self, serializer):
    #     # Дополнительная логика при создании, если medical_record_id не передается в теле запроса
    #     # medical_record = get_object_or_404(MedicalRecord, pk=self.kwargs['medical_record_pk'])
    #     # serializer.save(medical_record=medical_record)
    #     pass


class PrescribedMedicationViewSet(viewsets.ModelViewSet):
    queryset = PrescribedMedication.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return PrescribedMedicationCreateSerializer
        return PrescribedMedicationSerializer

    def get_queryset(self):
        return PrescribedMedication.objects.all()


class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return VitalSignCreateSerializer
        return VitalSignSerializer

    def get_queryset(self):
        return VitalSign.objects.all()


class PatientDocumentViewSet(viewsets.ModelViewSet):
    queryset = PatientDocument.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return PatientDocumentCreateSerializer
        return PatientDocumentSerializer

    def get_queryset(self):
        return PatientDocument.objects.all()

    def perform_create(self, serializer):
        # medical_record_id должен быть передан в теле запроса через PatientDocumentCreateSerializer
        # uploaded_by устанавливается автоматически из request.user
        serializer.save(uploaded_by=self.request.user)
