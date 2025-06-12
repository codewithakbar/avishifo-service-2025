from django.db import models
from accounts.models import User
from hospitals.models import Hospital

class Doctor(models.Model):
    SPECIALTIES = (
        ('internal_medicine', 'Терапия (внутренние болезни)'),
        ('cardiology', 'Кардиология'),
        ('endocrinology', 'Эндокринология'),
        ('pulmonology', 'Пульмонология'),
        ('gastroenterology', 'Гастроэнтерология'),
        ('nephrology', 'Нефрология'),
        ('hematology', 'Гематология'),
        ('rheumatology', 'Ревматология'),
        ('allergy_immunology', 'Аллергология и иммунология'),
        ('infectious_diseases', 'Инфекционные болезни'),
        ('general_surgery', 'Общая хирургия'),
        ('cardiovascular_surgery', 'Сердечно-сосудистая хирургия'),
        ('neurosurgery', 'Нейрохирургия'),
        ('orthopedics_traumatology', 'Ортопедия и травматология'),
        ('urology', 'Урология'),
        ('plastic_surgery', 'Пластическая хирургия'),
        ('pediatric_surgery', 'Детская хирургия'),
        ('oncological_surgery', 'Онкохирургия'),
        ('thoracic_surgery', 'Торакальная хирургия'),
        ('maxillofacial_surgery', 'Челюстно-лицевая хирургия'),
        ('obstetrics_gynecology', 'Акушерство и гинекология'),
        ('pediatrics', 'Педиатрия'),
        ('neurology', 'Неврология'),
        ('psychiatry', 'Психиатрия'),
        ('dermatovenereology', 'Дерматовенерология'),
        ('ophthalmology', 'Офтальмология'),
        ('otolaryngology', 'Отоларингология (ЛОР)'),
        ('dentistry', 'Стоматология'),
        ('radiology', 'Радиология'),
        ('ultrasound_diagnostics', 'Ультразвуковая диагностика'),
        ('laboratory_diagnostics', 'Лабораторная диагностика'),
        ('pathomorphology', 'Патоморфология (патанатомия)'),
        ('functional_diagnostics', 'Функциональная диагностика'),
        ('medical_genetics', 'Медицинская генетика'),
        ('medical_rehabilitation', 'Медицинская реабилитация'),
        ('geriatrics', 'Гериатрия'),
        ('palliative_care', 'Паллиативная медицина'),
        ('sports_medicine', 'Спортивная медицина'),
        ('clinical_oncology', 'Клиническая онкология'),
        ('medical_cybernetics_ai', 'Медицинская кибернетика и ИИ в медицине'),
        ('transplantology', 'Трансплантология'),
        ('reproductive_medicine', 'Репродуктивная медицина'),
    )

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_id = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    license_number = models.CharField(max_length=50, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    years_of_experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.get_specialty_display()}"
    
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            # Generate doctor ID
            last_doctor = Doctor.objects.order_by('-id').first()
            if last_doctor:
                last_id = int(last_doctor.doctor_id[1:])
                self.doctor_id = f"D{last_id + 1:06d}"
            else:
                self.doctor_id = "D000001"
        super().save(*args, **kwargs)

class DoctorSchedule(models.Model):
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['doctor', 'day_of_week']
    
    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.get_day_of_week_display()}"
