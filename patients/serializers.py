from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import MedicalHistoryItem, MedicalRecord, Patient, PatientDocument, PatientVaqtincha, PrescribedMedication, VitalSign




class PatientVaqtinchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVaqtincha
        fields = '__all__'
        extra_kwargs = {
            'full_name': {'required': True},
            'passport_series': {'required': True},
            'passport_number': {'required': True},
        }




class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ("patient_id", "created_at", "updated_at")


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "blood_type",
            "emergency_contact_name",
            "emergency_contact_phone",
            "medical_history",
            "allergies",
            "current_medications",
            "insurance_number",
        )


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "blood_type",
            "emergency_contact_name",
            "emergency_contact_phone",
            "medical_history",
            "allergies",
            "current_medications",
            "insurance_number",
        )


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "user_type"]


class MedicalHistoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistoryItem
        fields = "__all__"
        read_only_fields = ["medical_record"]


class PrescribedMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribedMedication
        fields = "__all__"
        read_only_fields = ["medical_record"]


class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = "__all__"
        read_only_fields = ["medical_record"]


class PatientDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = BasicUserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PatientDocument
        fields = [
            "id",
            "medical_record",
            "document_name",
            "file",
            "file_url",
            "description",
            "uploaded_at",
            "uploaded_by",
        ]
        read_only_fields = ["medical_record", "uploaded_by", "file_url"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)  # Для чтения
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source="patient", write_only=True
    )  # Для записи

    doctor = BasicUserSerializer(read_only=True)  # Для чтения
    # doctor_id будет устанавливаться автоматически из request.user

    history_items = MedicalHistoryItemSerializer(many=True, read_only=True)
    prescriptions = PrescribedMedicationSerializer(many=True, read_only=True)
    vital_signs = VitalSignSerializer(many=True, read_only=True)
    documents = PatientDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            "id",
            "patient",
            "patient_id",
            "doctor",
            "encounter_date",
            "chief_complaint",
            "diagnosis",
            "treatment_plan",
            "notes",
            "history_items",
            "prescriptions",
            "vital_signs",
            "documents",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["doctor", "encounter_date", "created_at", "updated_at"]

    # Если вы хотите разрешить создание вложенных объектов при создании MedicalRecord:
    # def create(self, validated_data):
    #     # Логика для создания вложенных объектов
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     # Логика для обновления вложенных объектов
    #     return super().update(instance, validated_data)


# Сериализаторы для отдельных CRUD операций с элементами медкарты
class MedicalRecordItemCreateSerializerBase(serializers.ModelSerializer):
    medical_record_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        medical_record_id = validated_data.pop("medical_record_id")
        medical_record = MedicalRecord.objects.get(id=medical_record_id)
        # Проверка прав доступа (например, что текущий доктор имеет доступ к этой медкарте)
        # request = self.context.get('request')
        # if medical_record.doctor != request.user:
        #     raise serializers.ValidationError("У вас нет прав для добавления записи в эту медкарту.")
        validated_data["medical_record"] = medical_record
        return self.Meta.model.objects.create(**validated_data)


class MedicalHistoryItemCreateSerializer(MedicalRecordItemCreateSerializerBase):
    class Meta:
        model = MedicalHistoryItem
        exclude = [
            "medical_record"
        ]  # medical_record будет установлен из medical_record_id


class PrescribedMedicationCreateSerializer(MedicalRecordItemCreateSerializerBase):
    class Meta:
        model = PrescribedMedication
        exclude = ["medical_record"]


class VitalSignCreateSerializer(MedicalRecordItemCreateSerializerBase):
    class Meta:
        model = VitalSign
        exclude = ["medical_record"]


class PatientDocumentCreateSerializer(MedicalRecordItemCreateSerializerBase):
    uploaded_by_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PatientDocument
        exclude = ["medical_record", "uploaded_by"]
        extra_kwargs = {"file": {"required": True}}
