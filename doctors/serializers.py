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


class DoctorProfilePageSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for the doctor profile page
    Matches all frontend requirements from the profile page
    """
    # User fields
    full_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone_number', read_only=True)
    profile_picture = serializers.SerializerMethodField()
    
    # Professional fields
    specialization = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    education = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    languages = serializers.SerializerMethodField()
    certifications = serializers.CharField(required=False, allow_blank=True)
    
    # Personal fields
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    region = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, allow_blank=True)
    
    # Contact fields
    emergency_contact = serializers.CharField(required=False, allow_blank=True)
    medical_license = serializers.CharField(required=False, allow_blank=True)
    insurance = serializers.CharField(required=False, allow_blank=True)
    
    # Schedule fields
    working_hours = serializers.CharField(required=False, allow_blank=True)
    consultation_fee = serializers.SerializerMethodField()
    availability = serializers.CharField(required=False, allow_blank=True)
    
    # Statistics fields
    total_patients = serializers.IntegerField(read_only=True)
    monthly_consultations = serializers.IntegerField(read_only=True)
    rating = serializers.SerializerMethodField()
    total_reviews = serializers.IntegerField(read_only=True)
    years_experience = serializers.IntegerField(source='years_of_experience', read_only=True)
    completed_treatments = serializers.IntegerField(read_only=True)
    active_patients = serializers.IntegerField(read_only=True)
    monthly_income = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    languages_spoken = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()
    awards = serializers.SerializerMethodField()
    research_papers = serializers.IntegerField(read_only=True)
    conferences_attended = serializers.IntegerField(read_only=True)
    
    # Location field (computed)
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            # User fields
            'full_name', 'first_name', 'last_name', 'email', 'phone', 'profile_picture',
            # Professional fields
            'specialization', 'experience', 'education', 'bio', 'languages', 'certifications',
            # Personal fields
            'date_of_birth', 'gender', 'address', 'country', 'region', 'district',
            # Contact fields
            'emergency_contact', 'medical_license', 'insurance',
            # Schedule fields
            'working_hours', 'consultation_fee', 'availability',
            # Statistics fields
            'total_patients', 'monthly_consultations', 'rating', 'total_reviews',
            'years_experience', 'completed_treatments', 'active_patients', 'monthly_income',
            'languages_spoken', 'specializations', 'awards', 'research_papers', 'conferences_attended',
            # Computed fields
            'location'
        ]
    
    def get_full_name(self, obj):
        if obj.user.full_name:
            return obj.user.full_name
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    
    def get_profile_picture(self, obj):
        if obj.user.profile_picture:
            return obj.user.profile_picture.url
        return None
    
    def get_specialization(self, obj):
        if obj.specialty:
            return obj.get_specialty_display()
        return "Врач"
    
    def get_experience(self, obj):
        years = obj.years_of_experience
        if years == 0:
            return "Опыт не указан"
        elif years == 1:
            return f"{years} год"
        elif years < 5:
            return f"{years} года"
        else:
            return f"{years} лет"
    
    def get_languages(self, obj):
        if obj.languages_spoken:
            if isinstance(obj.languages_spoken, list):
                return obj.languages_spoken
            elif isinstance(obj.languages_spoken, str):
                return [lang.strip() for lang in obj.languages_spoken.split(',') if lang.strip()]
        return []
    
    def get_consultation_fee(self, obj):
        if obj.consultation_fee:
            return f"{obj.consultation_fee:,.0f} сум"
        return "Не указано"
    
    def get_rating(self, obj):
        if obj.rating:
            return f"{obj.rating:.1f}"
        return "4.9"  # Default rating
    
    def get_languages_spoken(self, obj):
        return self.get_languages(obj)
    
    def get_specializations(self, obj):
        if obj.specializations:
            return obj.specializations
        return []
    
    def get_awards(self, obj):
        if obj.awards:
            return obj.awards
        return []
    
    def get_location(self, obj):
        location_parts = []
        if obj.address:
            location_parts.append(obj.address)
        if obj.district:
            location_parts.append(obj.district)
        if obj.region:
            location_parts.append(obj.region)
        if obj.country:
            location_parts.append(obj.country)
        
        if location_parts:
            return ", ".join(location_parts)
        return "Адрес не указан"
    
    def update(self, instance, validated_data):
        # Update user fields
        user = instance.user
        user_fields = ['first_name', 'last_name', 'email', 'phone_number']
        for field in user_fields:
            if field in validated_data:
                setattr(user, field, validated_data[field])
        user.save()
        
        # Update doctor fields
        for field, value in validated_data.items():
            if field not in user_fields and hasattr(instance, field):
                setattr(instance, field, value)
        
        instance.save()
        return instance


class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating doctor profile from the frontend
    Handles all the fields that can be updated via the profile page
    """
    # User fields that can be updated
    full_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    
    # Professional fields
    specialization = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    experience = serializers.CharField(required=False, allow_blank=True)
    education = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    languages = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    certifications = serializers.CharField(required=False, allow_blank=True)
    
    # Personal fields
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    region = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, allow_blank=True)
    
    # Contact fields
    emergency_contact = serializers.CharField(required=False, allow_blank=True)
    medical_license = serializers.CharField(required=False, allow_blank=True)
    insurance = serializers.CharField(required=False, allow_blank=True)
    
    # Schedule fields
    working_hours = serializers.CharField(required=False, allow_blank=True)
    consultation_fee = serializers.CharField(required=False, allow_blank=True)
    availability = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Doctor
        fields = [
            'full_name', 'email', 'phone', 'profile_picture',
            'specialization', 'experience', 'education', 'bio', 'languages', 'certifications',
            'date_of_birth', 'gender', 'address', 'country', 'region', 'district',
            'emergency_contact', 'medical_license', 'insurance',
            'working_hours', 'consultation_fee', 'availability'
        ]
    
    def update(self, instance, validated_data):
        # Handle full_name by updating first_name and last_name
        if 'full_name' in validated_data:
            full_name = validated_data.pop('full_name')
            if full_name:
                name_parts = full_name.strip().split(' ', 1)
                if len(name_parts) >= 2:
                    instance.user.first_name = name_parts[0]
                    instance.user.last_name = name_parts[1]
                else:
                    instance.user.first_name = full_name
                    instance.user.last_name = ""
                instance.user.save()
        
        # Handle email and phone updates
        if 'email' in validated_data:
            instance.user.email = validated_data.pop('email')
            instance.user.save()
        
        if 'phone' in validated_data:
            instance.user.phone_number = validated_data.pop('phone')
            instance.user.save()
        
        # Handle profile_picture updates
        if 'profile_picture' in validated_data:
            instance.user.profile_picture = validated_data.pop('profile_picture')
            instance.user.save()
        
        # Handle specialization (convert list to string for storage)
        if 'specialization' in validated_data:
            specializations = validated_data.pop('specialization')
            if isinstance(specializations, list):
                instance.specializations = specializations
                # Also update the main specialty if there's at least one
                if specializations:
                    instance.specialty = specializations[0]
        
        # Handle languages (convert list to string for storage)
        if 'languages' in validated_data:
            languages = validated_data.pop('languages')
            if isinstance(languages, list):
                instance.languages_spoken = languages
        
        # Handle consultation_fee (convert string to decimal)
        if 'consultation_fee' in validated_data:
            fee_str = validated_data.pop('consultation_fee')
            if fee_str and fee_str != "Не указано":
                try:
                    # Remove "сум" and commas, then convert to decimal
                    fee_clean = fee_str.replace('сум', '').replace(',', '').strip()
                    if fee_clean:
                        instance.consultation_fee = float(fee_clean)
                except (ValueError, TypeError):
                    pass
        
        # Update all other fields
        for field, value in validated_data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        
        instance.save()
        return instance
