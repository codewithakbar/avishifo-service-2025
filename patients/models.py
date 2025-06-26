from django.db import models
from django.conf import settings  # Для ссылки на User модель

# Предполагается, что у вас есть модель Doctor в приложении doctors
# from doctors.models import Doctor
# Если модель Doctor в том же приложении accounts, что и User:
from accounts.models import (
    User as DoctorUser,
)  # Предполагаем, что User модель используется для докторов

# Если у вас отдельная модель Doctor, импортируйте ее правильно
# Например, если Doctor в doctors.models:
# from doctors.models import Doctor


class Patient(models.Model):
    BLOOD_TYPES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )

    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "Женский"),
        ("other", "Другой"),
    ]

    user = models.OneToOneField(DoctorUser, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=20, unique=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=17, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient: {self.user.full_name} ({self.patient_id})"
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            last_patient = Patient.objects.order_by('-id').first()
            if last_patient:
                last_id = int(last_patient.patient_id[1:])
                self.patient_id = f"P{last_id + 1:06d}"
            else:
                self.patient_id = "P000001"
        super().save(*args, **kwargs)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_medical_records"
    )
    # Используем AUTH_USER_MODEL для доктора, если доктора - это пользователи с определенной ролью
    # Если у вас есть отдельная модель Doctor, замените settings.AUTH_USER_MODEL на Doctor
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="authored_patient_medical_records",
        limit_choices_to={"user_type__in": ["doctor"]},
    )
    encounter_date = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.TextField(help_text="Основная жалоба пациента")
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Дополнительные заметки врача")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-encounter_date"]

    def __str__(self):
        return f"Мед. карта для {self.patient.user.get_full_name()} от {self.encounter_date.strftime('%Y-%m-%d')}"


class MedicalHistoryItem(models.Model):
    medical_record = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE, related_name="patient_history_items"
    )
    ENTRY_TYPE_CHOICES = [
        ("condition", "Состояние/Заболевание"),
        ("surgery", "Операция"),
        ("family_history", "Семейный анамнез"),
        ("lifestyle", "Образ жизни"),
        ("other", "Другое"),
    ]
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPE_CHOICES)
    description = models.TextField()
    date_occurred = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_entry_type_display()}: {self.description[:50]}"


class PrescribedMedication(models.Model):
    medical_record = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE, related_name="patient_prescriptions"
    )
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, help_text="Например, 500мг, 1 таблетка")
    frequency = models.CharField(
        max_length=100, help_text="Например, 2 раза в день, перед едой"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(
        blank=True, help_text="Дополнительные инструкции по приему"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication_name} ({self.dosage})"


class VitalSign(models.Model):
    medical_record = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE, related_name="patient_vital_signs"
    )
    measurement_time = models.DateTimeField(auto_now_add=True)
    blood_pressure_systolic = models.PositiveIntegerField(
        null=True, blank=True, help_text="Верхнее давление (мм рт.ст.)"
    )
    blood_pressure_diastolic = models.PositiveIntegerField(
        null=True, blank=True, help_text="Нижнее давление (мм рт.ст.)"
    )
    heart_rate = models.PositiveIntegerField(
        null=True, blank=True, help_text="Пульс (уд/мин)"
    )
    temperature_celsius = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Температура (°C)",
    )
    respiratory_rate = models.PositiveIntegerField(
        null=True, blank=True, help_text="Частота дыхания (вдохов/мин)"
    )
    oxygen_saturation = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Сатурация кислорода (%)",
    )
    height_cm = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True, help_text="Рост (см)"
    )
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True, help_text="Вес (кг)"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Показатели от {self.measurement_time.strftime('%Y-%m-%d %H:%M')}"


class PatientDocument(models.Model):
    medical_record = models.ForeignKey(
        MedicalRecord, on_delete=models.CASCADE, related_name="patient_documents"
    )
    document_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="patient_documents/%Y/%m/%d/")
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_patient_docs",
    )

    def __str__(self):
        return self.document_name
