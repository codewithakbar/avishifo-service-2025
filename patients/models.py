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


class PatientVaqtincha(models.Model):
    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "Женский"),
    ]

    BLOOD_GROUP_CHOICES = [
        ("A+", "A(II) Rh+"),
        ("A-", "A(II) Rh-"),
        ("B+", "B(III) Rh+"),
        ("B-", "B(III) Rh-"),
        ("AB+", "AB(IV) Rh+"),
        ("AB-", "AB(IV) Rh-"),
        ("O+", "O(I) Rh+"),
        ("O-", "O(I) Rh-"),
    ]

    full_name = models.CharField(max_length=255)  # ФИО
    passport_series = models.CharField(max_length=10)
    passport_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(null=True, blank=True)  # 🆕 Tug'ilgan sana
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    secondary_phone = models.CharField(
        max_length=20, null=True, blank=True
    )  # 🆕 Ikkinchi telefon
    blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('archived', 'Архивный'),
        ('deleted', 'Удаленный'),
    ]
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    archived_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')

    def __str__(self):
        return self.full_name


class KasallikTarixi(models.Model):
    patient = models.ForeignKey(
        to=PatientVaqtincha,
        on_delete=models.CASCADE,
        related_name="kasalliklar",
    )
    fish = models.CharField("F.I.SH", max_length=255)
    tugilgan_sana = models.DateField("Tug'ilgan sana")
    millati = models.CharField("Millati", max_length=100, blank=True)
    malumoti = models.CharField("Ma'lumoti", max_length=100, blank=True)
    kasbi = models.CharField("Kasbi", max_length=100, blank=True)
    ish_joyi = models.CharField("Ish joyi", max_length=255, blank=True)
    ish_vazifasi = models.CharField("Ish joyidagi vazifasi", max_length=255, blank=True)
    uy_manzili = models.CharField("Uy manzili", max_length=255, blank=True)
    kelgan_vaqti = models.DateField("Kelgan vaqti")
    shikoyatlar = models.TextField("Kelgan vaqtdagi shikoyatlari", blank=True)

    asosiy_kasalliklar = models.TextField("Asosiy tizimli kasalliklari", blank=True)
    asosiy_kasalliklar_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/asosiy_kasalliklar/", null=True, blank=True
    )

    nafas_tizimi = models.TextField(blank=True)
    nafas_tizimi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/nafas_tizimi/", null=True, blank=True
    )

    yotal = models.TextField("Yo'tal", blank=True)
    yotal_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/yotal/", null=True, blank=True
    )

    balgam = models.TextField("Balg'am", blank=True)
    balgam_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/balgam/", null=True, blank=True
    )

    qon_tuflash = models.TextField(blank=True)
    qon_tuflash_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/qon_tuflash/", null=True, blank=True
    )

    kokrak_ogriq = models.TextField("Ko'krak qafasidagi og'riq", blank=True)
    kokrak_ogriq_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/kokrak_ogriq/", null=True, blank=True
    )

    nafas_qisishi = models.TextField(blank=True)
    nafas_qisishi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/nafas_qisishi/", null=True, blank=True
    )

    yurak_qon_shikoyatlari = models.TextField(blank=True)
    yurak_qon_shikoyatlari_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/yurak_qon_shikoyatlari/", null=True, blank=True
    )

    yurak_ogriq = models.TextField(blank=True)
    yurak_ogriq_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/yurak_ogriq/", null=True, blank=True
    )

    yurak_urishi_ozgarishi = models.TextField(blank=True)
    yurak_urishi_ozgarishi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/yurak_urishi_ozgarishi/", null=True, blank=True
    )

    yurak_urishi_sezish = models.TextField(blank=True)
    yurak_urishi_sezish_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/yurak_urishi_sezish/", null=True, blank=True
    )

    hazm_tizimi = models.TextField(blank=True)
    hazm_tizimi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/hazm_tizimi/", null=True, blank=True
    )

    qusish = models.TextField(blank=True)
    qusish_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/qusish/", null=True, blank=True
    )

    qorin_ogriq = models.TextField(blank=True)
    qorin_ogriq_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/qorin_ogriq/", null=True, blank=True
    )

    qorin_shish = models.TextField(blank=True)
    qorin_shish_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/qorin_shish/", null=True, blank=True
    )

    ich_ozgarishi = models.TextField(blank=True)
    ich_ozgarishi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/ich_ozgarishi/", null=True, blank=True
    )

    anus_shikoyatlar = models.TextField(blank=True)
    anus_shikoyatlar_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/anus_shikoyatlar/", null=True, blank=True
    )

    siydik_tizimi = models.TextField("Siydik ajratish tizimi faoliyati", blank=True)
    siydik_tizimi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/siydik_tizimi/", null=True, blank=True
    )

    endokrin_tizimi = models.TextField(blank=True)
    endokrin_tizimi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/endokrin_tizimi/", null=True, blank=True
    )

    tayanch_tizimi = models.TextField(blank=True)
    tayanch_tizimi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/tayanch_tizimi/", null=True, blank=True
    )

    asab_tizimi = models.TextField(blank=True)
    asab_tizimi_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/asab_tizimi/", null=True, blank=True
    )

    doktor_tavsiyalari = models.TextField(blank=True)
    doktor_tavsiyalari_hujjat = models.FileField(
        upload_to="kasallik_hujjatlari/doktor_tavsiyalari/", null=True, blank=True
    )

    # Qo'shimcha ma'lumotlar (Life History)
    zararli_odatlar = models.TextField("Zararli odatlar", blank=True)
    oilaviy_anamnez = models.TextField("Oilaviy anamnez", blank=True)
    allergiyalar = models.TextField("Allergiyalar", blank=True)
    otkazilgan_kasalliklar = models.TextField("O'tkazilgan kasalliklar", blank=True)

    # Fizikal ko'rik (Examination)
    umumiy_korik = models.TextField("Umumiy ko'rik", blank=True)
    bosh_boyin = models.TextField("Bosh va bo'yin", blank=True)
    teri = models.TextField("Teri holati", blank=True)
    limfa_tugunlari = models.TextField("Limfa tugunlari", blank=True)
    qorin_palpatsiyasi = models.TextField("Qorin palpatsiyasi", blank=True)
    perkussiya = models.TextField("Perkussiya", blank=True)
    opka_auskultatsiyasi = models.TextField("O'pka auskultatsiyasi", blank=True)
    yurak_auskultatsiyasi = models.TextField("Yurak auskultatsiyasi", blank=True)
    qorin_auskultatsiyasi = models.TextField("Qorin auskultatsiyasi", blank=True)

    ai_tahlil = models.TextField("AI tahlili va tashxisi", blank=True)

    yuborilgan_vaqt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fish


class Patient(models.Model):
    BLOOD_TYPES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )

    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "Женский"),
        ("other", "Другой"),
    ]

    user = models.OneToOneField(
        DoctorUser, on_delete=models.CASCADE, related_name="patient_profile"
    )
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
            last_patient = Patient.objects.order_by("-id").first()
            if last_patient:
                last_id = int(last_patient.patient_id[1:])
                self.patient_id = f"P{last_id + 1:06d}"
            else:
                self.patient_id = "P000001"
        super().save(*args, **kwargs)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        PatientVaqtincha, on_delete=models.CASCADE, related_name="patient_medical_records"
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
