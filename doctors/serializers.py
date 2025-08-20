from rest_framework import serializers
from accounts.models import User
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
    gender_label = serializers.SerializerMethodField()
    
    # Profile statistics and computed fields
    total_patients = serializers.SerializerMethodField()
    total_consultations = serializers.SerializerMethodField()
    formatted_income = serializers.SerializerMethodField()
    formatted_rating = serializers.SerializerMethodField()
    experience_years_text = serializers.SerializerMethodField()

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
            "gender_label",
            "reviews_count",
            "patients_accepted_count",
            "consultations_count",
            "documents_verified_status",
            "last_verification_date",
            "total_patients",
            "total_consultations",
            "formatted_income",
            "formatted_rating",
            "experience_years_text",
        )

    def get_specialty_label(self, obj):
        return obj.get_specialty_display() if obj.specialty else "Не указано"

    def get_category_label(self, obj):
        return obj.get_category_display()

    def get_degree_label(self, obj):
        return obj.get_degree_display()

    def get_gender_label(self, obj):
        return obj.get_gender_display()

    def get_total_patients(self, obj):
        return obj.patients_accepted_count

    def get_total_consultations(self, obj):
        return obj.consultations_count

    def get_formatted_income(self, obj):
        if obj.total_income:
            if obj.total_income >= 1000000:
                return f"{obj.total_income / 1000000:.1f}M"
            elif obj.total_income >= 1000:
                return f"{obj.total_income / 1000:.1f}K"
            else:
                return f"{obj.total_income:.0f}"
        return "0"

    def get_formatted_rating(self, obj):
        return f"{obj.rating:.1f}" if obj.rating else "0.0"

    def get_experience_years_text(self, obj):
        years = obj.years_of_experience
        if years == 0:
            return "Опыт не указан"
        elif years == 1:
            return f"{years} год"
        elif years < 5:
            return f"{years} года"
        else:
            return f"{years} лет"

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
            "bio",
            "specializations",
            "gender",
            "emergency_contact",
            "insurance_info",
            "working_hours",
            "availability_status",
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
            "bio",
            "specializations",
            "gender",
            "emergency_contact",
            "insurance_info",
            "working_hours",
            "availability_status",
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


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password",)
        read_only_fields = ["is_verified", "date_joined", "is_staff", "is_superuser"]


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    # SPECIALTIES map
    SPECIALTY_KEYS = [k for k, _ in Doctor.SPECIALTIES]

    # Allow any input in list, validate manually
    specializations = serializers.ListField(
        child=serializers.JSONField(), required=False  # <-- fix: allows dict or string
    )

    def validate_specializations(self, value):
        """
        Accepts either list of strings or list of dicts with 'value'.
        Converts to list of strings (values) and validates.
        """
        result = []
        for item in value:
            if isinstance(item, dict):
                val = item.get("value")
            else:
                val = item

            if val not in self.SPECIALTY_KEYS:
                raise serializers.ValidationError(f"Invalid specialization: {val}")
            result.append(val)
        return result

    def to_representation(self, instance):
        data = super().to_representation(instance)
        label_map = dict(Doctor.SPECIALTIES)
        data["specializations"] = [
            {"value": val, "label": label_map.get(val, val)}
            for val in instance.specializations or []
        ]
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Doctor
        exclude = ["doctor_id", "created_at", "updated_at"]


class DoctorListSerializer(serializers.ModelSerializer):
    """Serializer for listing doctors with essential information"""
    user = serializers.SerializerMethodField()
    specialty_label = serializers.SerializerMethodField()
    hospital_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'doctor_id', 'user', 'specialty_label', 'hospital_name',
            'years_of_experience', 'rating', 'consultation_fee', 'is_available',
            'patients_accepted_count', 'consultations_count'
        ]
    
    def get_user(self, obj):
        return {
            'full_name': obj.user.full_name,
            'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
            'email': obj.user.email,
            'phone_number': obj.user.phone_number,
        }
    
    def get_specialty_label(self, obj):
        return obj.get_specialty_display() if obj.specialty else "Не указано"
    
    def get_hospital_name(self, obj):
        return obj.hospital.name if obj.hospital else None


class DoctorDetailSerializer(serializers.ModelSerializer):
    """Comprehensive serializer for detailed doctor view"""
    user = UserSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)
    
    # Computed fields for UI
    specialty_label = serializers.SerializerMethodField()
    category_label = serializers.SerializerMethodField()
    degree_label = serializers.SerializerMethodField()
    gender_label = serializers.SerializerMethodField()
    experience_text = serializers.SerializerMethodField()
    income_formatted = serializers.SerializerMethodField()
    formatted_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = "__all__"
    
    def get_specialty_label(self, obj):
        return obj.get_specialty_display() if obj.specialty else "Не указано"
    
    def get_category_label(self, obj):
        return obj.get_category_display()
    
    def get_degree_label(self, obj):
        return obj.get_degree_display()
    
    def get_gender_label(self, obj):
        return obj.get_gender_display()
    
    def get_experience_text(self, obj):
        years = obj.years_of_experience
        if years == 0:
            return "Опыт не указан"
        elif years == 1:
            return f"{years} год"
        elif years < 5:
            return f"{years} года"
        else:
            return f"{years} лет"
    
    def get_income_formatted(self, obj):
        if obj.total_income:
            if obj.total_income >= 1000000:
                return f"{obj.total_income / 1000000:.1f}M"
            elif obj.total_income >= 1000:
                return f"{obj.total_income / 1000:.1f}K"
            else:
                return f"{obj.total_income:.0f}"
        return "0"
    
    def get_formatted_rating(self, obj):
        return f"{obj.rating:.1f}" if obj.rating else "0.0"
