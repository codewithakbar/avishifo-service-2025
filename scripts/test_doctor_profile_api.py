#!/usr/bin/env python
"""
Test script for Doctor Profile Management API
Demonstrates GET, PUT, and PATCH methods for all profile information fields
"""

import os
import sys
import django
import json
from datetime import date

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_api.settings')
django.setup()

from doctors.models import Doctor, Hospital
from doctors.serializers import DoctorDetailSerializer
from accounts.models import User


def print_separator(title):
    """Print a formatted separator with title"""
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)


def print_response_info(method, endpoint, data=None, response=None):
    """Print formatted API call information"""
    print(f"\n🔗 {method} {endpoint}")
    if data:
        print(f"📤 Request Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    if response:
        print(f"📥 Response: {json.dumps(response, indent=2, ensure_ascii=False)}")


def create_sample_data():
    """Create sample doctor data for testing"""
    print_separator("Creating Sample Data")
    
    # Create hospital
    hospital, created = Hospital.objects.get_or_create(
        name="Республиканская клиническая больница",
        defaults={
            'address': "Улица Марифатчи, Хорезмский область, Узбекистан",
            'phone': "+998901234567"
        }
    )
    print(f"✅ Hospital: {hospital.name}")
    
    # Create user
    user, created = User.objects.get_or_create(
        username="akbar_doctor_test",
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
    print(f"✅ User: {user.full_name}")
    
    # Create doctor
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
            'Сертификат по эхокардиографии'
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
            'linkedin': 'https://linkedin.com/in/akbar-tugayevich'
        },
        'bio': 'Опытный кардиолог с 15-летним стажем работы.',
        'specializations': ['echocardiography', 'interventional_cardiology'],
        'gender': 'male',
        'emergency_contact': '+998901234568',
        'insurance_info': 'Принимаю все основные страховые полисы',
        'working_hours': 'Понедельник - Пятница: 09:00-17:00',
        'availability_status': 'Доступен для консультаций',
        'total_income': 4500000.00,
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
            if key != 'user':
                setattr(doctor, key, value)
        doctor.save()
    
    print(f"✅ Doctor: {doctor.user.full_name} - {doctor.get_specialty_display()}")
    return doctor


def test_get_profile():
    """Test GET method for retrieving doctor profile"""
    print_separator("Testing GET Profile API")
    
    print("📋 This would be a GET request to: /api/doctors/profile/")
    print("🔐 Requires authentication (doctor must be logged in)")
    
    # Simulate the response data
    doctor = Doctor.objects.first()
    if doctor:
        serializer = DoctorDetailSerializer(doctor)
        response_data = {
            "success": True,
            "message": "Doctor profile retrieved successfully",
            "data": serializer.data
        }
        
        print_response_info("GET", "/api/doctors/profile/", response=response_data)
        
        # Show key profile information
        data = serializer.data
        print("\n📊 Profile Summary:")
        print(f"   👤 Full Name: {data['user']['first_name']} {data['user']['last_name']}")
        print(f"   📧 Email: {data['user']['email']}")
        print(f"   🏥 Specialty: {data['specialty_label']}")
        print(f"   ⏰ Experience: {data['experience_text']}")
        print(f"   ⭐ Rating: {data['formatted_rating']}")
        print(f"   💰 Income: {data['income_formatted']}")
        print(f"   🏥 Hospital: {data['hospital']['name'] if data['hospital'] else 'Не указано'}")
        
        return response_data
    else:
        print("❌ No doctor found for testing")
        return None


def test_put_profile():
    """Test PUT method for complete profile update"""
    print_separator("Testing PUT Profile API")
    
    print("📋 This would be a PUT request to: /api/doctors/profile/")
    print("🔐 Requires authentication (doctor must be logged in)")
    
    # Sample complete update data
    update_data = {
        "user": {
            "first_name": "Akbar",
            "last_name": "Tugayevich",
            "email": "akbar.updated@gmail.com",
            "phone_number": "+998901234567",
            "date_of_birth": "1990-06-12",
            "address": "Улица Марифатчи, Хорезмский область, Узбекистан"
        },
        "specialty": "cardiology",
        "years_of_experience": 16,
        "education": "Ташкентский медицинский институт, 2010 - Обновлено",
        "consultation_fee": "180000.00",
        "category": "higher",
        "degree": "phd",
        "bio": "Опытный кардиолог с 16-летним стажем работы. Специализируюсь на диагностике и лечении сердечно-сосудистых заболеваний. Обновленная биография.",
        "specializations": ["echocardiography", "interventional_cardiology", "preventive_cardiology"],
        "gender": "male",
        "emergency_contact": "+998901234568",
        "insurance_info": "Принимаю все основные страховые полисы. Работаю с ведущими страховыми компаниями.",
        "working_hours": "Понедельник - Пятница: 09:00-18:00, Суббота: 09:00-14:00",
        "availability_status": "Доступен для консультаций по предварительной записи",
        "languages_spoken": ["Русский", "Узбекский", "Английский", "Немецкий"],
        "work_email": "akbar.cardio.updated@hospital.uz",
        "work_phone": "+998901234567",
        "social_media_links": {
            "linkedin": "https://linkedin.com/in/akbar-tugayevich",
            "researchgate": "https://researchgate.net/profile/akbar-tugayevich"
        },
        "consultation_schedule": {
            "monday": "09:00-18:00",
            "tuesday": "09:00-18:00",
            "wednesday": "09:00-18:00",
            "thursday": "09:00-18:00",
            "friday": "09:00-18:00",
            "saturday": "09:00-14:00"
        },
        "online_consultation_available": True,
        "certifications": [
            "Сертификат кардиолога высшей категории - Обновлено",
            "Сертификат по эхокардиографии - Обновлено",
            "Сертификат по интервенционной кардиологии - Новый"
        ]
    }
    
    print_response_info("PUT", "/api/doctors/profile/", data=update_data)
    
    print("\n📝 This request would:")
    print("   ✅ Update all user information (name, email, phone, etc.)")
    print("   ✅ Update all doctor professional information")
    print("   ✅ Update work schedule and availability")
    print("   ✅ Update contact information and social media")
    print("   ✅ Update certifications and specializations")
    
    return update_data


def test_patch_profile():
    """Test PATCH method for partial profile update"""
    print_separator("Testing PATCH Profile API")
    
    print("📋 This would be a PATCH request to: /api/doctors/profile/")
    print("🔐 Requires authentication (doctor must be logged in)")
    
    # Sample partial update data
    partial_update_data = {
        "bio": "Обновленная биография с новыми достижениями и специализациями.",
        "consultation_fee": "200000.00",
        "working_hours": "Понедельник - Пятница: 09:00-19:00, Суббота: 09:00-15:00",
        "availability_status": "Доступен по предварительной записи, возможны экстренные консультации",
        "emergency_contact": "+998901234569",
        "insurance_info": "Расширенный список страховых компаний, включая международные"
    }
    
    print_response_info("PATCH", "/api/doctors/profile/", data=partial_update_data)
    
    print("\n📝 This request would:")
    print("   ✅ Update only specific fields (bio, consultation fee, working hours)")
    print("   ✅ Keep all other fields unchanged")
    print("   ✅ Update emergency contact and insurance information")
    print("   ✅ Modify availability status")
    
    return partial_update_data


def test_profile_fields_info():
    """Test GET method for profile fields information"""
    print_separator("Testing Profile Fields Info API")
    
    print("📋 This would be a GET request to: /api/doctors/profile/fields/")
    print("🔐 Requires authentication")
    
    # Simulate the response data
    fields_info = {
        "success": True,
        "message": "Profile fields information retrieved successfully",
        "data": {
            "personal_information": {
                "full_name": {"type": "string", "source": "user.first_name + user.last_name", "required": True},
                "email": {"type": "email", "source": "user.email", "required": True},
                "bio": {"type": "text", "source": "bio", "required": False},
                "date_of_birth": {"type": "date", "source": "user.date_of_birth", "required": False},
                "gender": {"type": "choice", "source": "gender", "required": False, "choices": {
                    "male": "Мужской",
                    "female": "Женский",
                    "other": "Другой",
                    "not_specified": "Не указано"
                }},
                "languages_spoken": {"type": "json_array", "source": "languages_spoken", "required": False},
            },
            "professional_information": {
                "specialty": {"type": "choice", "source": "specialty", "required": False, "choices": {
                    "cardiology": "Кардиология",
                    "neurology": "Неврология",
                    "pediatrics": "Педиатрия"
                }},
                "years_of_experience": {"type": "integer", "source": "years_of_experience", "required": False},
                "education": {"type": "text", "source": "education", "required": False},
                "certifications": {"type": "json_array", "source": "certifications", "required": False},
                "license_number": {"type": "string", "source": "license_number", "required": False},
                "insurance_info": {"type": "text", "source": "insurance_info", "required": False},
            },
            "work_schedule": {
                "working_hours": {"type": "text", "source": "working_hours", "required": False},
                "availability_status": {"type": "string", "source": "availability_status", "required": False},
                "consultation_fee": {"type": "decimal", "source": "consultation_fee", "required": False},
            },
            "contact_information": {
                "phone": {"type": "string", "source": "user.phone_number", "required": False},
                "emergency_contact": {"type": "string", "source": "emergency_contact", "required": False},
                "address": {"type": "text", "source": "user.address", "required": False},
            }
        }
    }
    
    print_response_info("GET", "/api/doctors/profile/fields/", response=fields_info)
    
    print("\n📋 This endpoint provides:")
    print("   ✅ Field types and validation rules")
    print("   ✅ Required vs optional fields")
    print("   ✅ Available choices for dropdown fields")
    print("   ✅ Field source mapping")
    print("   ✅ Frontend form generation support")
    
    return fields_info


def test_api_endpoints_summary():
    """Show summary of all available API endpoints"""
    print_separator("Available API Endpoints")
    
    endpoints = [
        {
            "method": "GET",
            "endpoint": "/api/doctors/profile/",
            "description": "Get complete doctor profile",
            "authentication": "Required",
            "response": "Full profile data with computed fields"
        },
        {
            "method": "PUT",
            "endpoint": "/api/doctors/profile/",
            "description": "Update complete doctor profile",
            "authentication": "Required",
            "request": "Complete profile data",
            "response": "Updated profile data"
        },
        {
            "method": "PATCH",
            "endpoint": "/api/doctors/profile/",
            "description": "Partially update doctor profile",
            "authentication": "Required",
            "request": "Partial profile data",
            "response": "Updated profile data"
        },
        {
            "method": "GET",
            "endpoint": "/api/doctors/profile/fields/",
            "description": "Get profile fields information",
            "authentication": "Required",
            "response": "Field types, validation rules, choices"
        },
        {
            "method": "GET",
            "endpoint": "/api/doctors/",
            "description": "List all doctors",
            "authentication": "Required",
            "response": "List of doctor summaries"
        },
        {
            "method": "GET",
            "endpoint": "/api/doctors/{id}/",
            "description": "Get specific doctor details",
            "authentication": "Required",
            "response": "Complete doctor profile"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n🔗 {endpoint['method']} {endpoint['endpoint']}")
        print(f"   📝 {endpoint['description']}")
        print(f"   🔐 {endpoint['authentication']}")
        if 'request' in endpoint:
            print(f"   📤 {endpoint['request']}")
        print(f"   📥 {endpoint['response']}")


def main():
    """Main function to run all tests"""
    print_separator("Doctor Profile Management API Testing")
    print("This script demonstrates the API endpoints for doctor profile management")
    print("All endpoints require authentication and are designed for the logged-in doctor")
    
    try:
        # Create sample data
        doctor = create_sample_data()
        
        # Test all API methods
        test_get_profile()
        test_put_profile()
        test_patch_profile()
        test_profile_fields_info()
        
        # Show API endpoints summary
        test_api_endpoints_summary()
        
        print_separator("Testing Complete")
        print("✅ All API methods demonstrated successfully!")
        print("\n📚 Next steps:")
        print("   1. Test the actual API endpoints with your frontend")
        print("   2. Implement proper error handling")
        print("   3. Add field validation as needed")
        print("   4. Test with different user types and permissions")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
