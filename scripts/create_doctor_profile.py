#!/usr/bin/env python
"""
Script to create a doctor profile for user ID 1 if it doesn't exist
This will fix the "Doctor profile not found" error
"""

import os
import sys
import django
from datetime import date
import uuid

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_api.settings')
django.setup()

from doctors.models import Doctor, Hospital
from accounts.models import User


def generate_unique_medical_identifier():
    """Generate a unique medical identifier"""
    # Try to find an unused identifier
    for i in range(1, 1000):
        identifier = f"CARD{i:03d}"
        if not Doctor.objects.filter(medical_identifier=identifier).exists():
            return identifier
    
    # If all are taken, use UUID
    return f"CARD_{str(uuid.uuid4())[:8].upper()}"


def check_and_create_doctor_profile():
    """Check if doctor profile exists for user ID 1, create if not"""
    print("🔍 Checking for existing doctor profile...")
    
    try:
        # Check if user ID 1 exists
        user = User.objects.filter(id=1).first()
        if not user:
            print("❌ User with ID 1 does not exist")
            return False
        
        print(f"✅ Found user: {user.username} ({user.first_name} {user.last_name})")
        print(f"   User type: {user.user_type}")
        
        # Check if doctor profile exists
        try:
            doctor = Doctor.objects.get(user=user)
            print(f"✅ Doctor profile already exists: {doctor.doctor_id}")
            print(f"   Specialty: {doctor.get_specialty_display() if doctor.specialty else 'Not specified'}")
            return True
        except Doctor.DoesNotExist:
            print("❌ No doctor profile found for this user")
            
            # Create hospital if it doesn't exist
            hospital, created = Hospital.objects.get_or_create(
                name="Республиканская клиническая больница",
                defaults={
                    'address': "Улица Марифатчи, Хорезмский область, Узбекистан",
                    'phone': "+998901234567"
                }
            )
            if created:
                print(f"✅ Created hospital: {hospital.name}")
            else:
                print(f"✅ Using existing hospital: {hospital.name}")
            
            # Generate unique medical identifier
            medical_identifier = generate_unique_medical_identifier()
            print(f"✅ Generated unique medical identifier: {medical_identifier}")
            
            # Create doctor profile
            doctor_data = {
                'user': user,
                'specialty': 'cardiology',  # Default specialty
                'license_number': f'MD{uuid.uuid4().hex[:6].upper()}',
                'hospital': hospital,
                'years_of_experience': 15,
                'education': 'Ташкентский медицинский институт, 2010',
                'consultation_fee': 150000.00,
                'category': 'higher',
                'main_workplace': 'Республиканская клиническая больница',
                'medical_identifier': medical_identifier,
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
            
            doctor = Doctor.objects.create(**doctor_data)
            print(f"✅ Created doctor profile: {doctor.doctor_id}")
            print(f"   Specialty: {doctor.get_specialty_display()}")
            print(f"   Experience: {doctor.years_of_experience} years")
            print(f"   Rating: {doctor.rating}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_profile_endpoint():
    """Test if the profile endpoint now works"""
    print("\n🧪 Testing profile endpoint...")
    
    try:
        from doctors.serializers import DoctorDetailSerializer
        
        # Get the doctor profile
        doctor = Doctor.objects.filter(user_id=1).first()
        if doctor:
            serializer = DoctorDetailSerializer(doctor)
            data = serializer.data
            
            print("✅ Profile endpoint test successful!")
            print(f"   Doctor ID: {data['doctor_id']}")
            print(f"   Name: {data['user']['first_name']} {data['user']['last_name']}")
            print(f"   Specialty: {data['specialty_label']}")
            print(f"   Experience: {data['experience_text']}")
            print(f"   Rating: {data['formatted_rating']}")
            
            return True
        else:
            print("❌ No doctor profile found for testing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing profile endpoint: {e}")
        return False


def main():
    """Main function"""
    print("🚀 Doctor Profile Creation Script")
    print("=" * 50)
    
    # Check and create doctor profile
    success = check_and_create_doctor_profile()
    
    if success:
        print("\n✅ Doctor profile setup completed successfully!")
        
        # Test the profile endpoint
        test_profile_endpoint()
        
        print("\n📋 Next steps:")
        print("   1. Try accessing /api/doctors/profile/ again")
        print("   2. The endpoint should now return the doctor profile")
        print("   3. You can use GET, PUT, and PATCH methods")
        
    else:
        print("\n❌ Failed to setup doctor profile")
        print("   Check the error messages above")


if __name__ == "__main__":
    main()
