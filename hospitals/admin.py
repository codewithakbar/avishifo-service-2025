from django.contrib import admin
from django.utils.html import format_html
from .models import Hospital, Department


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    fields = ("name", "head_doctor", "is_active")
    autocomplete_fields = ["head_doctor"]


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "email",
        "bed_capacity",
        "emergency_services",
        "get_total_doctors",
        "is_active",
        "established_date",
    )
    list_filter = (
        "emergency_services",
        "is_active",
        "established_date",
        "bed_capacity",
        "created_at",
    )
    search_fields = (
        "name",
        "address",
        "phone_number",
        "email",
        "license_number",
        "website",
    )
    readonly_fields = ("total_doctors", "available_doctors", "created_at", "updated_at")
    ordering = ("name",)
    inlines = [DepartmentInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "address", "phone_number", "email", "website")},
        ),
        (
            "Legal & Operational",
            {
                "fields": (
                    "license_number",
                    "established_date",
                    "bed_capacity",
                    "emergency_services",
                    "is_active",
                )
            },
        ),
        (
            "Statistics",
            {
                "fields": ("total_doctors", "available_doctors"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_total_doctors(self, obj):
        return obj.total_doctors

    get_total_doctors.short_description = "Total Doctors"

    actions = ["activate_hospitals", "deactivate_hospitals"]

    def activate_hospitals(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} hospitals were activated.")

    activate_hospitals.short_description = "Activate selected hospitals"

    def deactivate_hospitals(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} hospitals were deactivated.")

    deactivate_hospitals.short_description = "Deactivate selected hospitals"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_hospital_name",
        "get_head_doctor",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "hospital", "created_at")
    search_fields = (
        "name",
        "description",
        "hospital__name",
        "head_doctor__user__first_name",
        "head_doctor__user__last_name",
    )
    ordering = ("hospital", "name")

    fieldsets = (
        (
            "Department Information",
            {"fields": ("hospital", "name", "description", "head_doctor")},
        ),
        ("Status", {"fields": ("is_active",)}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_hospital_name(self, obj):
        return obj.hospital.name

    get_hospital_name.short_description = "Hospital"
    get_hospital_name.admin_order_field = "hospital__name"

    def get_head_doctor(self, obj):
        if obj.head_doctor:
            return f"Dr. {obj.head_doctor.user.full_name}"
        return "-"

    get_head_doctor.short_description = "Head Doctor"
    get_head_doctor.admin_order_field = "head_doctor__user__first_name"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("hospital", "head_doctor__user")
        )

    autocomplete_fields = ["hospital", "head_doctor"]
