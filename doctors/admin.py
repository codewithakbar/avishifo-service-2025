from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Doctor, DoctorSchedule, Hospital, Specialization  


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = (
        'label',
        'value',
        'get_doctors_count',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('label', 'value', 'description')
    list_editable = ('is_active',)  # Tezkor tahrirlash uchun
    ordering = ('label',)
    readonly_fields = ('created_at', 'updated_at', 'get_doctors_count_display')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "value",
                    "label",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "Статистика",
            {
                "fields": ("get_doctors_count_display",),
                "classes": ("collapse",),
            },
        ),
        (
            "Временные метки",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    
    actions = ['activate_specializations', 'deactivate_specializations']
    
    def get_doctors_count(self, obj):
        """Ko'rsatish: qancha doktor bu specializationni ishlatayotgani"""
        # Annotate qilingan bo'lsa, undan foydalanish
        if hasattr(obj, 'doctors__count'):
            count = obj.doctors__count
        else:
            count = obj.doctors.count()
        
        if count > 0:
            return format_html(
                '<a href="/admin/doctors/doctor/?specializations__id__exact={}" style="color: #417690; font-weight: bold;">{}</a>',
                obj.id,
                count
            )
        return mark_safe('<span style="color: #999;">0</span>')
    
    get_doctors_count.short_description = "Количество врачей"
    get_doctors_count.admin_order_field = "doctors__count"
    
    def get_doctors_count_display(self, obj):
        """Detail view uchun ko'rsatish"""
        if obj.pk:
            count = obj.doctors.count()
            return f"{count} врачей используют эту специализацию"
        return "Специализация еще не создана"
    
    get_doctors_count_display.short_description = "Используется врачами"
    
    def activate_specializations(self, request, queryset):
        """Faollashtirish action"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f"{updated} специализаций было активировано."
        )
    
    activate_specializations.short_description = "Активировать выбранные специализации"
    
    def deactivate_specializations(self, request, queryset):
        """Deaktivatsiya qilish action"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} специализаций было деактивировано."
        )
    
    deactivate_specializations.short_description = "Деактивировать выбранные специализации"
    
    def get_queryset(self, request):
        """Optimizatsiya: doctors count bilan"""
        queryset = super().get_queryset(request)
        # Annotate qilish list_display uchun
        if 'get_doctors_count' in self.list_display:
            queryset = queryset.annotate(doctors__count=Count('doctors'))
        return queryset


class DoctorScheduleInline(admin.TabularInline):
    model = DoctorSchedule
    extra = 0
    fields = ("day_of_week", "start_time", "end_time", "is_available")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_id",
        "get_full_name",
        "specialty",
        "get_hospital_name",
        "years_of_experience",
        "consultation_fee",
        "rating",
        "is_available",
        "gender",
        "category",
    )
    list_filter = (
        "specialty",
        "specializations",  # ManyToMany filter
        "hospital",
        "is_available",
        "years_of_experience",
        "gender",
        "category",
        "degree",
        "created_at",
        "user__is_verified",
    )
    search_fields = (
        "doctor_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "license_number",
        "hospital__name",
        "specialty",
        "bio",
        "main_workplace",
    )
    readonly_fields = ("doctor_id", "rating", "created_at", "updated_at", "total_income")
    ordering = ("-created_at",)
    inlines = [DoctorScheduleInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("doctor_id", "user", "gender", "date_of_birth")},
        ),
        (
            "Professional Information",
            {
                "fields": (
                    "specialty",
                    "specializations",
                    "license_number",
                    "category",
                    "degree",
                    "years_of_experience",
                    "education",
                    "certifications",
                    "bio",
                )
            },
        ),
        (
            "Work Details",
            {
                "fields": (
                    "hospital",
                    "main_workplace",
                    "medical_identifier",
                    "consultation_fee",
                    "total_income",
                )
            },
        ),
        (
            "Schedule & Availability",
            {
                "fields": (
                    "is_available",
                    "availability_status",
                    "working_hours",
                    "consultation_schedule",
                    "online_consultation_available",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "work_email",
                    "work_phone",
                    "emergency_contact",
                    "social_media_links",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "languages_spoken",
                    "insurance_info",
                    "rating",
                    "reviews_count",
                    "patients_accepted_count",
                    "consultations_count",
                )
            },
        ),
        (
            "Verification & Analytics",
            {
                "fields": (
                    "documents_verified_status",
                    "last_verification_date",
                    "last_reviews",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_full_name(self, obj):
        return f"Dr. {obj.user.full_name}"

    get_full_name.short_description = "Full Name"
    get_full_name.admin_order_field = "user__first_name"

    def get_hospital_name(self, obj):
        return obj.hospital.name if obj.hospital else "Не указано"

    get_hospital_name.short_description = "Hospital"
    get_hospital_name.admin_order_field = "hospital__name"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "hospital")

    autocomplete_fields = ["user", "hospital"]
    filter_horizontal = ["specializations"]  # ManyToMany field uchun qulay interface

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = Doctor._meta.get_field(
                "user"
            ).related_model.objects.filter(user_type="doctor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ["make_available", "make_unavailable"]

    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} doctors were marked as available.")

    make_available.short_description = "Mark selected doctors as available"

    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} doctors were marked as unavailable.")

    make_unavailable.short_description = "Mark selected doctors as unavailable"


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "get_doctor_name",
        "day_of_week",
        "start_time",
        "end_time",
        "is_available",
    )
    list_filter = ("day_of_week", "is_available", "doctor__specialty")
    search_fields = (
        "doctor__user__first_name",
        "doctor__user__last_name",
        "doctor__doctor_id",
        "day_of_week",
    )
    ordering = ("doctor", "day_of_week")

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.full_name}"

    get_doctor_name.short_description = "Doctor"
    get_doctor_name.admin_order_field = "doctor__user__first_name"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("doctor__user")

    autocomplete_fields = ["doctor"]
