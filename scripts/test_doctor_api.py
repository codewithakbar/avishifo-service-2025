#!/usr/bin/env python
"""
Test script to demonstrate the updated Doctor model and serializers
This script shows how to create, update, and retrieve doctor profiles with all the new fields
"""

import os
import sys
import django
from datetime import date

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_api.settings')
django.setup()

from doctors.models import Doctor, Hospital
from doctors.serializers import DoctorSerializer, DoctorCreateSerializer, DoctorUpdateSerializer, DoctorProfileSerializer
from accounts.models import User


def create_sample_hospital():
    """Create a sample hospital for testing"""
    hospital, created = Hospital.objects.get_or_create(
        name="Республиканская клиническая больница",
        defaults={
            'address': "Улица Марифатчи, Хорезмский область, Узбекистан",
            'phone': "+998901234567"
        }
    )
    return hospital


def create_sample_user():
    """Create a sample user for testing"""
    user, created = User.objects.get_or_create(
        username="akbar_doctor",
        defaults={
            'first_name': 'Akbar',
            'last_name': 'Tugayevich',
            'email': 'satipovakbar@gmail.com',
            'user_type': 'doctor',
            'phone_number': '+998901234567',
            'date_of_birth': date(1990, 6, 12),
            'address': 'Улица Марифатчи, Хорезмский область, Узбекистан',
            'is_verified': True
        }
    )
    return user


def create_sample_doctor():
    """Create a sample doctor with all the new fields"""
    user = create_sample_user()
    hospital = create_sample_hospital()
    
    doctor_data = {
        'user': user,
        'specialty': 'cardiology',
        'license_number': 'MD123456',
        'hospital': hospital,
        'years_of_experience': 15,
        'education': 'Ташкентский медицинский институт, 2010',
        'consultation_fee': 150000.00,
        'category': 'higher',
        'main_workplace': 'Республиканская клиническая больница',
        'medical_identifier': 'CARD001',
        'degree': 'phd',
        'certifications': [
            'Сертификат кардиолога высшей категории',
            'Сертификат по эхокардиографии',
            'Сертификат по интервенционной кардиологии'
        ],
        'consultation_schedule': {
            'monday': '09:00-17:00',
            'tuesday': '09:00-17:00',
            'wednesday': '09:00-17:00',
            'thursday': '09:00-17:00',
            'friday': '09:00-17:00'
        },
        'online_consultation_available': True,
        'languages_spoken': ['Русский', 'Узбекский', 'Английский'],
        'work_email': 'akbar.cardio@hospital.uz',
        'work_phone': '+998901234567',
        'social_media_links': {
            'linkedin': 'https://linkedin.com/in/akbar-tugayevich',
            'researchgate': 'https://researchgate.net/profile/akbar-tugayevich'
        },
        'bio': 'Опытный кардиолог с 15-летним стажем работы. Специализируюсь на диагностике и лечении сердечно-сосудистых заболеваний.',
        'specializations': ['echocardiography', 'interventional_cardiology', 'preventive_cardiology'],
        'gender': 'male',
        'emergency_contact': '+998901234568',
        'insurance_info': 'Принимаю все основные страховые полисы',
        'working_hours': 'Понедельник - Пятница: 09:00-17:00, Суббота: 09:00-13:00',
        'availability_status': 'Доступен для консультаций',
        'total_income': 4500000.00,  # 4.5M
        'rating': 4.9,
        'reviews_count': 127,
        'patients_accepted_count': 127,
        'consultations_count': 89
    }
    
    doctor, created = Doctor.objects.get_or_create(
        user=user,
        defaults=doctor_data
    )
    
    if not created:
        # Update existing doctor with new data
        for key, value in doctor_data.items():
            if key != 'user':  # Don't change the user
                setattr(doctor, key, value)
        doctor.save()
    
    return doctor


def test_doctor_serializer():
    """Test the DoctorSerializer with all fields"""
    print("=== Testing DoctorSerializer ===")
    
    doctor = create_sample_doctor()
    serializer = DoctorSerializer(doctor)
    data = serializer.data
    
    print(f"Doctor ID: {data['doctor_id']}")
    print(f"Full Name: {data['user']['full_name']}")
    print(f"Specialty: {data['specialty_label']}")
    print(f"Experience: {data['experience_years_text']}")
    print(f"Rating: {data['formatted_rating']}")
    print(f"Total Patients: {data['total_patients']}")
    print(f"Total Consultations: {data['total_consultations']}")
    print(f"Income: {data['formatted_income']}")
    print(f"Gender: {data['gender_label']}")
    print(f"Category: {data['category_label']}")
    print(f"Degree: {data['degree_label']}")
    print(f"Bio: {data['bio']}")
    print(f"Working Hours: {data['working_hours']}")
    print(f"Emergency Contact: {data['emergency_contact']}")
    print(f"Insurance: {data['insurance_info']}")
    print(f"Languages: {data['languages_spoken']}")
    print(f"Specializations: {data['specializations']}")
    print(f"Consultation Schedule: {data['consultation_schedule']}")
    print(f"Social Media: {data['social_media_links']}")
    print(f"Availability Status: {data['availability_status']}")
    print(f"Total Income: {data['total_income']}")
    print(f"Created At: {data['created_at']}")
    print(f"Updated At: {data['updated_at']}")


def test_doctor_create_serializer():
    """Test the DoctorCreateSerializer"""
    print("\n=== Testing DoctorCreateSerializer ===")
    
    create_data = {
        'specialty': 'neurology',
        'license_number': 'MD789012',
        'years_of_experience': 8,
        'education': 'Самаркандский медицинский институт, 2015',
        'consultation_fee': 120000.00,
        'category': 'first',
        'degree': 'none',
        'bio': 'Молодой невролог, специализирующийся на лечении заболеваний нервной системы.',
        'gender': 'female',
        'working_hours': 'Понедельник - Пятница: 08:00-16:00',
        'languages_spoken': ['Русский', 'Узбекский'],
        'online_consultation_available': True
    }
    
    serializer = DoctorCreateSerializer(data=create_data)
    if serializer.is_valid():
        print("Create serializer is valid!")
        print(f"Validated data: {serializer.validated_data}")
    else:
        print(f"Create serializer errors: {serializer.errors}")


def test_doctor_update_serializer():
    """Test the DoctorUpdateSerializer"""
    print("\n=== Testing DoctorUpdateSerializer ===")
    
    doctor = Doctor.objects.first()
    if doctor:
        update_data = {
            'bio': 'Обновленная биография с новыми достижениями',
            'consultation_fee': 180000.00,
            'working_hours': 'Понедельник - Пятница: 09:00-18:00, Суббота: 09:00-14:00',
            'availability_status': 'Доступен по предварительной записи'
        }
        
        serializer = DoctorUpdateSerializer(doctor, data=update_data, partial=True)
        if serializer.is_valid():
            print("Update serializer is valid!")
            print(f"Validated data: {serializer.validated_data}")
        else:
            print(f"Update serializer errors: {serializer.errors}")


def test_doctor_profile_serializer():
    """Test the DoctorProfileSerializer"""
    print("\n=== Testing DoctorProfileSerializer ===")
    
    doctor = Doctor.objects.first()
    if doctor:
        serializer = DoctorProfileSerializer(doctor)
        data = serializer.data
        
        print(f"Profile Data Keys: {list(data.keys())}")
        print(f"User Data: {data['user']}")
        print(f"Specializations: {data['specializations']}")


def main():
    """Main function to run all tests"""
    print("Starting Doctor Model and Serializer Tests...")
    print("=" * 50)
    
    try:
        test_doctor_serializer()
        test_doctor_create_serializer()
        test_doctor_update_serializer()
        test_doctor_profile_serializer()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
