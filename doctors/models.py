from django.db import models
from accounts.models import User

# from hospitals.models import Hospital # Agar Hospital modeli shu faylda bo'lmasa, uni import qilish kerak.
# Agar Hospital modeli yuqorida aniqlangan bo'lsa, bu importga hojat yo'q.


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой'),
        ('not_specified', 'Не указано'),
    )
    
    SPECIALTIES = (
        ("internal_medicine", "Терапия (внутренние болезни)"),
        ("cardiology", "Кардиология"),
        ("endocrinology", "Эндокринология"),
        ("pulmonology", "Пульмонология"),
        ("gastroenterology", "Гастроэнтерология"),
        ("nephrology", "Нефрология"),
        ("hematology", "Гематология"),
        ("rheumatology", "Ревматология"),
        ("allergy_immunology", "Аллергология и иммунология"),
        ("infectious_diseases", "Инфекционные болезни"),
        ("general_surgery", "Общая хирургия"),
        ("cardiovascular_surgery", "Сердечно-сосудистая хирургия"),
        ("neurosurgery", "Нейрохирургия"),
        ("orthopedics_traumatology", "Ортопедия и травматология"),
        ("urology", "Урология"),
        ("plastic_surgery", "Пластическая хирургия"),
        ("pediatric_surgery", "Детская хирургия"),
        ("oncological_surgery", "Онкохирургия"),
        ("thoracic_surgery", "Торакальная хирургия"),
        ("maxillofacial_surgery", "Челюстно-лицевая хирургия"),
        ("obstetrics_gynecology", "Акушерство и гинекология"),
        ("pediatrics", "Педиатрия"),
        ("neurology", "Неврология"),
        ("psychiatry", "Психиатрия"),
        ("dermatovenereology", "Дерматовенерология"),
        ("ophthalmology", "Офтальмология"),
        ("otolaryngology", "Отоларингология (ЛОР)"),
        ("dentistry", "Стоматология"),
        ("radiology", "Радиология"),
        ("ultrasound_diagnostics", "Ультразвуковая диагностика"),
        ("laboratory_diagnostics", "Лабораторная диагностика"),
        ("pathomorphology", "Патоморфология (патанатомия)"),
        ("functional_diagnostics", "Функциональная диагностика"),
        ("medical_genetics", "Медицинская генетика"),
        ("medical_rehabilitation", "Медицинская реабилитация"),
        ("geriatrics", "Гериатрия"),
        ("palliative_care", "Паллиативная медицина"),
        ("sports_medicine", "Спортивная медицина"),
        ("clinical_oncology", "Клиническая онкология"),
        ("medical_cybernetics_ai", "Медицинская кибернетика и ИИ в медицине"),
        ("transplantology", "Трансплантология"),
        ("reproductive_medicine", "Репродуктивная медицина"),
    )

    CATEGORY_CHOICES = (
        ("first", "Первая категория"),
        ("higher", "Высшая категория"),
        ("professor", "Профессор"),
        ("candidate", "Кандидат наук"),
        ("doctor_science", "Доктор наук"),
        ("no_category", "Без категории"),
    )

    DEGREE_CHOICES = (
        ("none", "Нет"),
        ("phd", "Кандидат наук (PhD)"),
        ("dsc", "Доктор наук (DSc)"),
        ("md", "Доктор медицины (MD)"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    doctor_id = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES, blank=True, null=True)
    license_number = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )  # Made nullable
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="doctors",
        blank=True,
        null=True,
    )  # Made nullable
    years_of_experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 1️⃣ Профессиональная информация
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="no_category"
    )
    main_workplace = models.CharField(max_length=255, blank=True, null=True)
    medical_identifier = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, default="none")
    certifications = models.JSONField(
        default=list, blank=True, null=True
    )  # Changed to JSONField

    # 2️⃣ График работы
    consultation_schedule = models.JSONField(
        default=dict, blank=True, null=True
    )  # e.g., {"Monday": "09:00-17:00"}
    online_consultation_available = models.BooleanField(default=False)
    languages_spoken = models.JSONField(
        default=list, blank=True, null=True
    )  # e.g., ["Русский", "Узбекский"]

    # 3️⃣ Дополнительные контакты
    work_email = models.EmailField(blank=True, null=True)
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    social_media_links = models.JSONField(
        default=dict, blank=True, null=True
    )  # e.g., {"linkedin": "url", "researchgate": "url"}

    # 4️⃣ Рейтинги и отзывы
    reviews_count = models.PositiveIntegerField(default=0)
    last_reviews = models.JSONField(
        default=list, blank=True, null=True
    )  # e.g., [{"patient": "Name", "text": "Review", "date": "YYYY-MM-DD"}]

    # 5️⃣ Информация для внутренней аналитики AviShifo
    patients_accepted_count = models.PositiveIntegerField(default=0)
    consultations_count = models.PositiveIntegerField(default=0)

    # 6️⃣ Безопасность и верификация
    documents_verified_status = models.BooleanField(default=False)
    last_verification_date = models.DateTimeField(blank=True, null=True)

    # 7️⃣ NEW FIELDS based on Frontend
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="A short biography or professional statement for the profile page."
    )
    specializations = models.JSONField(
        default=list,
        blank=True,
        help_text="A list of more specific specializations, e.g., ['Echocardiography', 'Interventional Cardiology']"
    )
    
    # 8️⃣ Additional profile fields from UI
    gender = models.CharField(
        max_length=20, 
        choices=GENDER_CHOICES, 
        default='not_specified',
        help_text="Пол врача"
    )
    emergency_contact = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Экстренный контакт"
    )
    insurance_info = models.TextField(
        blank=True, 
        null=True,
        help_text="Информация о страховке"
    )
    working_hours = models.TextField(
        blank=True, 
        null=True,
        help_text="Рабочие часы в текстовом формате"
    )
    availability_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Статус доступности (например: 'Доступен', 'В отпуске', 'Занят')"
    )
    total_income = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0.00,
        help_text="Общий доход врача"
    )

    # 9️⃣ NEW FIELDS from Frontend Profile Page
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        help_text="Дата рождения врача"
    )
    address = models.TextField(
        blank=True, 
        null=True,
        help_text="Полный адрес врача"
    )
    country = models.CharField(
        max_length=100,
        blank=True, 
        null=True,
        help_text="Страна"
    )
    region = models.CharField(
        max_length=100,
        blank=True, 
        null=True,
        help_text="Область/Регион"
    )
    district = models.CharField(
        max_length=100,
        blank=True, 
        null=True,
        help_text="Район"
    )
    medical_license = models.CharField(
        max_length=100,
        blank=True, 
        null=True,
        help_text="Медицинская лицензия"
    )
    insurance = models.TextField(
        blank=True, 
        null=True,
        help_text="Страховая информация"
    )
    availability = models.CharField(
        max_length=100,
        blank=True, 
        null=True,
        help_text="Доступность (например: 'Понедельник - Пятница')"
    )
    
    # 🔟 Statistics fields for frontend display
    total_patients = models.PositiveIntegerField(
        default=0,
        help_text="Общее количество пациентов"
    )
    monthly_consultations = models.PositiveIntegerField(
        default=0,
        help_text="Количество консультаций в месяц"
    )
    total_reviews = models.PositiveIntegerField(
        default=0,
        help_text="Общее количество отзывов"
    )
    completed_treatments = models.PositiveIntegerField(
        default=0,
        help_text="Завершенные курсы лечения"
    )
    active_patients = models.PositiveIntegerField(
        default=0,
        help_text="Активные пациенты"
    )
    monthly_income = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0.00,
        help_text="Месячный доход"
    )
    research_papers = models.PositiveIntegerField(
        default=0,
        help_text="Количество научных работ"
    )
    conferences_attended = models.PositiveIntegerField(
        default=0,
        help_text="Количество посещенных конференций"
    )
    awards = models.JSONField(
        default=list,
        blank=True,
        help_text="Награды и достижения"
    )

    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.get_specialty_display() if self.specialty else 'Специализация не указана'}"
    
    def save(self, *args, **kwargs):
        if not self.doctor_id:
            # Generate doctor ID
            last_doctor = Doctor.objects.order_by("-id").first()
            if last_doctor:
                last_id = int(last_doctor.doctor_id[1:])
                self.doctor_id = f"D{last_id + 1:06d}"
            else:
                self.doctor_id = "D000001"
        super().save(*args, **kwargs)


class DoctorSchedule(models.Model):
    DAYS_OF_WEEK = (
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
        ("sunday", "Sunday"),
    )

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="schedules"
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ["doctor", "day_of_week"]

    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.get_day_of_week_display()}"
