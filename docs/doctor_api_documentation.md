# Doctor API Documentation

## Overview

The Doctor API provides comprehensive functionality for managing doctor profiles in the AviShifo healthcare system. The updated model includes all the profile information fields shown in the UI, making it a complete solution for doctor profile management.

## Doctor Model Fields

### Basic Information
- `user` - OneToOneField to User model (doctor's account)
- `doctor_id` - Unique identifier (auto-generated)
- `gender` - Gender selection (male/female/other/not_specified)
- `date_of_birth` - Doctor's date of birth (from User model)

### Professional Information
- `specialty` - Primary medical specialty (from predefined choices)
- `specializations` - List of specific specializations
- `license_number` - Medical license number
- `category` - Professional category (first/higher/professor/candidate/doctor_science/no_category)
- `degree` - Academic degree (none/phd/dsc/md)
- `years_of_experience` - Years of professional experience
- `education` - Educational background
- `certifications` - List of professional certifications
- `bio` - Professional biography

### Work Details
- `hospital` - Associated hospital
- `main_workplace` - Primary workplace
- `medical_identifier` - Medical identifier
- `consultation_fee` - Fee for consultations
- `total_income` - Total income earned

### Schedule & Availability
- `is_available` - General availability status
- `availability_status` - Detailed availability description
- `working_hours` - Working hours in text format
- `consultation_schedule` - Detailed schedule (JSON)
- `online_consultation_available` - Online consultation availability

### Contact Information
- `work_email` - Professional email
- `work_phone` - Professional phone
- `emergency_contact` - Emergency contact number
- `social_media_links` - Social media profiles (JSON)

### Additional Information
- `languages_spoken` - Languages the doctor speaks
- `insurance_info` - Insurance information
- `rating` - Average rating
- `reviews_count` - Number of reviews
- `patients_accepted_count` - Number of patients
- `consultations_count` - Number of consultations

### Verification & Analytics
- `documents_verified_status` - Document verification status
- `last_verification_date` - Last verification date
- `last_reviews` - Recent reviews (JSON)

## Serializers

### 1. DoctorSerializer (Main Serializer)
**Purpose**: Complete doctor profile representation with computed fields

**Features**:
- All model fields
- Computed fields for UI display
- Human-readable labels for choices
- Formatted statistics

**Computed Fields**:
- `specialty_label` - Human-readable specialty name
- `category_label` - Human-readable category name
- `degree_label` - Human-readable degree name
- `gender_label` - Human-readable gender name
- `total_patients` - Total patient count
- `total_consultations` - Total consultation count
- `formatted_income` - Income in K/M format
- `formatted_rating` - Rating with one decimal place
- `experience_years_text` - Experience in Russian text format

**Usage**:
```python
# Get complete doctor profile
doctor = Doctor.objects.get(id=1)
serializer = DoctorSerializer(doctor)
data = serializer.data
```

### 2. DoctorCreateSerializer
**Purpose**: Creating new doctor profiles

**Fields**: All editable fields excluding read-only ones

**Usage**:
```python
data = {
    'specialty': 'cardiology',
    'years_of_experience': 15,
    'education': 'Medical University, 2010',
    'consultation_fee': 150000.00,
    'bio': 'Experienced cardiologist...',
    'gender': 'male',
    'working_hours': 'Monday-Friday: 9:00-17:00'
}

serializer = DoctorCreateSerializer(data=data)
if serializer.is_valid():
    doctor = serializer.save()
```

### 3. DoctorUpdateSerializer
**Purpose**: Updating existing doctor profiles

**Fields**: All editable fields with partial update support

**Usage**:
```python
doctor = Doctor.objects.get(id=1)
update_data = {
    'bio': 'Updated biography...',
    'consultation_fee': 180000.00
}

serializer = DoctorUpdateSerializer(doctor, data=update_data, partial=True)
if serializer.is_valid():
    doctor = serializer.save()
```

### 4. DoctorProfileSerializer
**Purpose**: Profile editing with nested user data

**Features**:
- Nested user data updates
- Specialization validation
- Profile-specific field handling

**Usage**:
```python
data = {
    'user': {
        'first_name': 'Akbar',
        'last_name': 'Tugayevich',
        'email': 'akbar@example.com'
    },
    'bio': 'Updated bio...',
    'specializations': ['echocardiography', 'interventional_cardiology']
}

serializer = DoctorProfileSerializer(doctor, data=data)
if serializer.is_valid():
    doctor = serializer.save()
```

### 5. DoctorListSerializer
**Purpose**: Efficient listing of doctors

**Features**:
- Essential information only
- Optimized for list views
- User data included

**Usage**:
```python
doctors = Doctor.objects.all()
serializer = DoctorListSerializer(doctors, many=True)
data = serializer.data
```

### 6. DoctorDetailSerializer
**Purpose**: Detailed doctor view

**Features**:
- Complete profile information
- All computed fields
- Optimized for detail views

**Usage**:
```python
doctor = Doctor.objects.get(id=1)
serializer = DoctorDetailSerializer(doctor)
data = serializer.data
```

## API Endpoints

### GET /api/doctors/
**Purpose**: List all doctors
**Serializer**: DoctorListSerializer
**Response**: List of doctor summaries

### GET /api/doctors/{id}/
**Purpose**: Get detailed doctor profile
**Serializer**: DoctorDetailSerializer
**Response**: Complete doctor profile

### POST /api/doctors/
**Purpose**: Create new doctor
**Serializer**: DoctorCreateSerializer
**Response**: Created doctor profile

### PUT /api/doctors/{id}/
**Purpose**: Update doctor profile
**Serializer**: DoctorUpdateSerializer
**Response**: Updated doctor profile

### PATCH /api/doctors/{id}/
**Purpose**: Partial update
**Serializer**: DoctorUpdateSerializer
**Response**: Updated doctor profile

### GET /api/doctors/{id}/profile/
**Purpose**: Get profile for editing
**Serializer**: DoctorProfileSerializer
**Response**: Profile data with user info

### PUT /api/doctors/{id}/profile/
**Purpose**: Update profile
**Serializer**: DoctorProfileSerializer
**Response**: Updated profile

## Example API Responses

### Doctor List Response
```json
[
    {
        "id": 1,
        "doctor_id": "D000001",
        "user": {
            "full_name": "Akbar Tugayevich",
            "profile_picture": "/media/profiles/akbar.jpg",
            "email": "satipovakbar@gmail.com",
            "phone_number": "+998901234567"
        },
        "specialty_label": "Кардиология",
        "hospital_name": "Республиканская клиническая больница",
        "years_of_experience": 15,
        "rating": 4.9,
        "consultation_fee": "150000.00",
        "is_available": true,
        "patients_accepted_count": 127,
        "consultations_count": 89
    }
]
```

### Doctor Detail Response
```json
{
    "id": 1,
    "doctor_id": "D000001",
    "user": {
        "id": 1,
        "username": "akbar_doctor",
        "first_name": "Akbar",
        "last_name": "Tugayevich",
        "email": "satipovakbar@gmail.com",
        "phone_number": "+998901234567",
        "date_of_birth": "1990-06-12",
        "address": "Улица Марифатчи, Хорезмский область, Узбекистан",
        "profile_picture": "/media/profiles/akbar.jpg",
        "is_verified": true
    },
    "specialty": "cardiology",
    "specialty_label": "Кардиология",
    "license_number": "MD123456",
    "hospital": {
        "id": 1,
        "name": "Республиканская клиническая больница",
        "address": "Улица Марифатчи, Хорезмский область, Узбекистан",
        "phone": "+998901234567"
    },
    "years_of_experience": 15,
    "experience_years_text": "15 лет",
    "education": "Ташкентский медицинский институт, 2010",
    "consultation_fee": "150000.00",
    "is_available": true,
    "rating": "4.9",
    "formatted_rating": "4.9",
    "category": "higher",
    "category_label": "Высшая категория",
    "degree": "phd",
    "degree_label": "Кандидат наук (PhD)",
    "main_workplace": "Республиканская клиническая больница",
    "medical_identifier": "CARD001",
    "certifications": [
        "Сертификат кардиолога высшей категории",
        "Сертификат по эхокардиографии",
        "Сертификат по интервенционной кардиологии"
    ],
    "consultation_schedule": {
        "monday": "09:00-17:00",
        "tuesday": "09:00-17:00",
        "wednesday": "09:00-17:00",
        "thursday": "09:00-17:00",
        "friday": "09:00-17:00"
    },
    "online_consultation_available": true,
    "languages_spoken": ["Русский", "Узбекский", "Английский"],
    "work_email": "akbar.cardio@hospital.uz",
    "work_phone": "+998901234567",
    "social_media_links": {
        "linkedin": "https://linkedin.com/in/akbar-tugayevich",
        "researchgate": "https://researchgate.net/profile/akbar-tugayevich"
    },
    "bio": "Опытный кардиолог с 15-летним стажем работы...",
    "specializations": ["echocardiography", "interventional_cardiology"],
    "gender": "male",
    "gender_label": "Мужской",
    "emergency_contact": "+998901234568",
    "insurance_info": "Принимаю все основные страховые полисы",
    "working_hours": "Понедельник - Пятница: 09:00-17:00, Суббота: 09:00-13:00",
    "availability_status": "Доступен для консультаций",
    "total_income": "4500000.00",
    "formatted_income": "4.5M",
    "reviews_count": 127,
    "last_reviews": [],
    "patients_accepted_count": 127,
    "total_patients": 127,
    "consultations_count": 89,
    "total_consultations": 89,
    "documents_verified_status": false,
    "last_verification_date": null,
    "created_at": "2025-01-27T10:00:00Z",
    "updated_at": "2025-01-27T10:00:00Z"
}
```

## Field Validation

### Required Fields
- `user` - Must be a valid User with user_type='doctor'
- `specialty` - Must be from predefined choices (can be null/blank)

### Optional Fields
- All other fields are optional and can be null/blank
- JSON fields accept appropriate data structures
- Date fields accept ISO format strings

### Validation Rules
- `consultation_fee` - Must be positive decimal
- `years_of_experience` - Must be non-negative integer
- `rating` - Must be between 0.00 and 5.00
- `total_income` - Must be positive decimal
- `phone` fields - Must match phone regex pattern

## Admin Interface

The Django admin interface has been updated to include all new fields organized in logical groups:

1. **Basic Information** - User, gender, date of birth
2. **Professional Information** - Specialty, education, certifications
3. **Work Details** - Hospital, workplace, fees
4. **Schedule & Availability** - Working hours, availability
5. **Contact Information** - Work contacts, emergency contact
6. **Additional Information** - Languages, insurance, statistics
7. **Verification & Analytics** - Verification status, reviews
8. **Timestamps** - Creation and update times

## Testing

Use the provided test script to verify all functionality:

```bash
python scripts/test_doctor_api.py
```

This script demonstrates:
- Creating sample data
- Testing all serializers
- Validating field handling
- Testing computed fields

## Migration Notes

The new fields were added in migration `0006_doctor_availability_status_doctor_emergency_contact_and_more.py`:

- Added: `gender`, `emergency_contact`, `insurance_info`, `working_hours`, `availability_status`, `total_income`
- Modified: `specialty` field to allow null/blank values
- All new fields are optional and won't affect existing data

## Best Practices

1. **Use appropriate serializers** for different operations
2. **Validate data** before saving
3. **Handle JSON fields** carefully (validate structure)
4. **Use computed fields** for UI display
5. **Implement proper error handling** for API responses
6. **Cache frequently accessed data** for performance
7. **Log important operations** for audit trails

## Support

For questions or issues with the Doctor API, refer to:
- Model definitions in `doctors/models.py`
- Serializer implementations in `doctors/serializers.py`
- Admin configuration in `doctors/admin.py`
- Test examples in `scripts/test_doctor_api.py`
