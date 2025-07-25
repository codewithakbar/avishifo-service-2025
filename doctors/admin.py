from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, DoctorSchedule, Hospital  


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    search_fields = ['name']


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
    )
    list_filter = (
        "specialty",
        "hospital",
        "is_available",
        "years_of_experience",
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
    )
    readonly_fields = ("doctor_id", "rating", "created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [DoctorScheduleInline]

    fieldsets = (
        (
            "Doctor Information",
            {"fields": ("doctor_id", "user", "specialty", "license_number")},
        ),
        (
            "Professional Details",
            {
                "fields": (
                    "hospital",
                    "years_of_experience",
                    "education",
                    "certifications",
                    "consultation_fee",
                )
            },
        ),
        ("Status & Rating", {"fields": ("is_available", "rating")}),
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
        return obj.hospital.name

    get_hospital_name.short_description = "Hospital"
    get_hospital_name.admin_order_field = "hospital__name"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "hospital")

    autocomplete_fields = ["user", "hospital"]

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
