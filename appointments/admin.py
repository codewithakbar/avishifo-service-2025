from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "get_patient_name",
        "get_doctor_name",
        "appointment_date",
        "appointment_type",
        "status",
        "fee",
        "duration_minutes",
    )
    list_filter = (
        "status",
        "appointment_type",
        "appointment_date",
        "doctor__specialty",
        "doctor__hospital",
        "created_at",
    )
    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "patient__patient_id",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "doctor__doctor_id",
        "reason",
    )
    readonly_fields = ("fee", "created_at", "updated_at")
    ordering = ("-appointment_date",)
    date_hierarchy = "appointment_date"

    fieldsets = (
        (
            "Appointment Details",
            {
                "fields": (
                    "patient",
                    "doctor",
                    "appointment_date",
                    "appointment_type",
                    "status",
                )
            },
        ),
        ("Medical Information", {"fields": ("reason", "notes")}),
        ("Billing & Duration", {"fields": ("duration_minutes", "fee")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_patient_name(self, obj):
        return obj.patient.user.full_name

    get_patient_name.short_description = "Patient"
    get_patient_name.admin_order_field = "patient__user__first_name"

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.full_name}"

    get_doctor_name.short_description = "Doctor"
    get_doctor_name.admin_order_field = "doctor__user__first_name"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("patient__user", "doctor__user", "doctor__hospital")
        )

    autocomplete_fields = ["patient", "doctor"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "appointment_date" in form.base_fields:
            form.base_fields["appointment_date"].help_text = (
                "Select future date and time"
            )
        return form

    actions = ["mark_completed", "mark_cancelled", "mark_confirmed"]

    def mark_completed(self, request, queryset):
        updated = queryset.update(status="completed")
        self.message_user(request, f"{updated} appointments were marked as completed.")

    mark_completed.short_description = "Mark selected appointments as completed"

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"{updated} appointments were cancelled.")

    mark_cancelled.short_description = "Cancel selected appointments"

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status="confirmed")
        self.message_user(request, f"{updated} appointments were confirmed.")

    mark_confirmed.short_description = "Confirm selected appointments"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj and obj.appointment_date < timezone.now():
            readonly_fields.extend(["appointment_date", "patient", "doctor"])
        return readonly_fields
