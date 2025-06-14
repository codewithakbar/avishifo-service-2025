from rest_framework import serializers
from accounts.serializers import UserSerializer
from hospitals.serializers import HospitalSerializer
from .models import Doctor, DoctorSchedule, Hospital


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)

    # Human-readable labels for choices
    specialty_label = serializers.SerializerMethodField()
    category_label = serializers.SerializerMethodField()
    degree_label = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = (
            "doctor_id",
            "rating",
            "created_at",
            "updated_at",
            "specialty_label",
            "category_label",
            "degree_label",
            "reviews_count",
            "patients_accepted_count",
            "consultations_count",
            "documents_verified_status",
            "last_verification_date",  # These are managed by backend logic
        )

    def get_specialty_label(self, obj):
        return obj.get_specialty_display()

    def get_category_label(self, obj):
        return obj.get_category_display()

    def get_degree_label(self, obj):
        return obj.get_degree_display()

    def create(self, validated_data):
        # Handle nested User and Hospital creation/association if needed
        # For now, assuming user and hospital are already created or passed as IDs
        # If user is passed via request.user in view, remove 'user' from validated_data
        # If hospital is passed as ID, it will be handled by default ModelSerializer behavior
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle nested updates if necessary
        return super().update(instance, validated_data)


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "specialty",
            "license_number",
            "hospital",
            "years_of_experience",
            "education",
            "certifications",
            "consultation_fee",
            "category",
            "main_workplace",
            "medical_identifier",
            "degree",
            "consultation_schedule",
            "online_consultation_available",
            "languages_spoken",
            "work_email",
            "work_phone",
            "social_media_links",
        )


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "specialty",
            "years_of_experience",
            "education",
            "certifications",
            "consultation_fee",
            "is_available",
            "category",
            "main_workplace",
            "medical_identifier",
            "degree",
            "consultation_schedule",
            "online_consultation_available",
            "languages_spoken",
            "work_email",
            "work_phone",
            "social_media_links",
            # Fields for internal analytics/verification, if they can be updated via API
            "reviews_count",
            "last_reviews",
            "patients_accepted_count",
            "consultations_count",
            "documents_verified_status",
            "last_verification_date",
        )
        read_only_fields = (
            "doctor_id",
            "rating",
            "created_at",
            "updated_at",
        )  # Ensure these are not updated directly


