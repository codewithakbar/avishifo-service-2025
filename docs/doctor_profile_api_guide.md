# Doctor Profile API Guide

Bu hujjat doctor profile sahifasi uchun yaratilgan API endpointlarni tavsiflaydi.

## Base URL
```
https://new.avishifo.uz/api/doctors/
```

## Authentication
Barcha API endpointlar JWT token talab qiladi. Token `Authorization` headerida yuborilishi kerak:
```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### 1. Doctor Profile Page - GET/PATCH
**URL:** `/profile/page/`  
**Method:** GET, PATCH  
**Description:** Doctor profile sahifasini ko'rish va yangilash

#### GET Response
```json
{
  "success": true,
  "message": "Doctor profile retrieved successfully",
  "data": {
    "full_name": "Доктор Ахмедов Алишер",
    "first_name": "Алишер",
    "last_name": "Ахмедов",
    "email": "alisher.ahmedov@example.com",
    "phone": "+998 90 123 45 67",
    "profile_picture": "/media/profiles/doctor.jpg",
    "specialization": "Кардиолог",
    "experience": "15 лет",
    "education": "Ташкентский медицинский университет",
    "bio": "Опытный кардиолог с 15-летним стажем работы...",
    "languages": ["Узбекский", "Русский", "Английский"],
    "certifications": "Сертификат кардиолога, Европейское общество кардиологов",
    "date_of_birth": "1985-03-15",
    "gender": "Мужской",
    "address": "Улица Марифатчи, дом 15",
    "country": "Узбекистан",
    "region": "Хорезмская",
    "district": "Ургенчский",
    "emergency_contact": "+998 90 987 65 43",
    "medical_license": "MD-12345",
    "insurance": "Страховая компания 'Медицинская защита'",
    "working_hours": "9:00-18:00",
    "consultation_fee": "150,000 сум",
    "availability": "Понедельник - Пятница",
    "total_patients": 127,
    "monthly_consultations": 89,
    "rating": "4.9",
    "total_reviews": 156,
    "years_experience": 15,
    "completed_treatments": 234,
    "active_patients": 45,
    "monthly_income": 4500000.00,
    "languages_spoken": ["Узбекский", "Русский", "Английский"],
    "specializations": ["Кардиология", "Эхокардиография", "ЭКГ"],
    "awards": ["Лучший врач года 2023", "Отличник здравоохранения"],
    "research_papers": 12,
    "conferences_attended": 28,
    "location": "Улица Марифатчи, дом 15, Ургенчский, Хорезмская, Узбекистан"
  }
}
```

#### PATCH Request
```json
{
  "full_name": "Доктор Ахмедов Алишер",
  "email": "alisher.ahmedov@example.com",
  "phone": "+998 90 123 45 67",
  "specialization": ["Кардиолог", "Эхокардиография"],
  "experience": "15 лет",
  "education": "Ташкентский медицинский университет",
  "bio": "Опытный кардиолог с 15-летним стажем работы...",
  "languages": ["Узбекский", "Русский", "Английский"],
  "certifications": "Сертификат кардиолога, Европейское общество кардиологов",
  "date_of_birth": "1985-03-15",
  "gender": "Мужской",
  "address": "Улица Марифатчи, дом 15",
  "country": "Узбекистан",
  "region": "Хорезмская",
  "district": "Ургенчский",
  "emergency_contact": "+998 90 987 65 43",
  "medical_license": "MD-12345",
  "insurance": "Страховая компания 'Медицинская защита'",
  "working_hours": "9:00-18:00",
  "consultation_fee": "150,000 сум",
  "availability": "Понедельник - Пятница"
}
```

### 2. Doctor Profile Statistics - GET
**URL:** `/profile/stats/`  
**Method:** GET  
**Description:** Doctor profile statistikalarini olish

#### Response
```json
{
  "success": true,
  "message": "Profile statistics retrieved successfully",
  "data": {
    "total_patients": 127,
    "monthly_consultations": 89,
    "rating": 4.9,
    "total_reviews": 156,
    "years_experience": 15,
    "completed_treatments": 234,
    "active_patients": 45,
    "monthly_income": 4500000.0,
    "research_papers": 12,
    "conferences_attended": 28,
    "total_income": 4500000.0
  }
}
```

### 3. Doctor Profile Fields Information - GET
**URL:** `/profile/fields-info/`  
**Method:** GET  
**Description:** Profile fieldlari haqida ma'lumot olish

#### Response
```json
{
  "success": true,
  "message": "Profile fields information retrieved successfully",
  "data": {
    "personal_information": {
      "full_name": {
        "type": "string",
        "source": "user.first_name + user.last_name",
        "required": true,
        "max_length": 255
      },
      "email": {
        "type": "email",
        "source": "user.email",
        "required": true,
        "max_length": 254
      },
      "phone": {
        "type": "string",
        "source": "user.phone_number",
        "required": false,
        "max_length": 20
      },
      "bio": {
        "type": "text",
        "source": "bio",
        "required": false,
        "max_length": null
      },
      "date_of_birth": {
        "type": "date",
        "source": "date_of_birth",
        "required": false
      },
      "gender": {
        "type": "choice",
        "source": "gender",
        "required": false,
        "choices": {
          "male": "Мужской",
          "female": "Женский",
          "other": "Другой",
          "not_specified": "Не указано"
        }
      },
      "address": {
        "type": "text",
        "source": "address",
        "required": false
      },
      "country": {
        "type": "string",
        "source": "country",
        "required": false,
        "max_length": 100
      },
      "region": {
        "type": "string",
        "source": "region",
        "required": false,
        "max_length": 100
      },
      "district": {
        "type": "string",
        "source": "district",
        "required": false,
        "max_length": 100
      }
    },
    "professional_information": {
      "specialization": {
        "type": "list",
        "source": "specializations",
        "required": false,
        "item_type": "string"
      },
      "experience": {
        "type": "string",
        "source": "experience",
        "required": false
      },
      "education": {
        "type": "text",
        "source": "education",
        "required": false
      },
      "certifications": {
        "type": "text",
        "source": "certifications",
        "required": false
      },
      "medical_license": {
        "type": "string",
        "source": "medical_license",
        "required": false,
        "max_length": 100
      },
      "insurance": {
        "type": "text",
        "source": "insurance",
        "required": false
      }
    },
    "work_schedule": {
      "working_hours": {
        "type": "string",
        "source": "working_hours",
        "required": false
      },
      "availability": {
        "type": "string",
        "source": "availability",
        "required": false,
        "max_length": 100
      },
      "consultation_fee": {
        "type": "string",
        "source": "consultation_fee",
        "required": false
      }
    },
    "contact_information": {
      "emergency_contact": {
        "type": "string",
        "source": "emergency_contact",
        "required": false,
        "max_length": 20
      }
    },
    "languages": {
      "languages": {
        "type": "list",
        "source": "languages_spoken",
        "required": false,
        "item_type": "string"
      }
    }
  }
}
```

### 4. Doctor Profile Options - GET
**URL:** `/profile/options/`  
**Method:** GET  
**Description:** Profile dropdown va selection uchun optionlarni olish

#### Response
```json
{
  "success": true,
  "message": "Profile options retrieved successfully",
  "data": {
    "languages": [
      "Узбекский", "Русский", "Казахский", "Киргизский", "Таджикский", "Туркменский",
      "Китайский", "Корейский", "Японский", "Вьетнамский", "Тайский", "Малайский",
      "Индонезийский", "Филиппинский", "Бенгальский", "Хинди", "Урду", "Персидский",
      "Арабский", "Турецкий", "Азербайджанский", "Грузинский", "Армянский",
      "Английский", "Немецкий", "Французский", "Испанский", "Итальянский", "Португальский",
      "Голландский", "Шведский", "Норвежский", "Датский", "Финский", "Польский",
      "Чешский", "Словацкий", "Венгерский", "Румынский", "Болгарский", "Сербский",
      "Хорватский", "Словенский", "Македонский", "Албанский", "Греческий",
      "Иврит", "Амхарский", "Суахили", "Зулу", "Африкаанс", "Хауса", "Йоруба"
    ],
    "working_hours": [
      "9:00-18:00", "8:00-17:00", "10:00-19:00", "9:00-17:00", "8:00-18:00",
      "10:00-18:00", "9:00-16:00", "8:00-16:00", "10:00-16:00", "24/7",
      "По вызову", "Гибкий график"
    ],
    "availability": [
      "Понедельник - Пятница", "Пн-Пт", "Понедельник - Суббота", "Пн-Сб",
      "Ежедневно", "По будням", "По выходным", "По записи", "Экстренные случаи",
      "24/7", "Гибкий график"
    ],
    "countries": [
      "Узбекистан", "Россия", "Казахстан"
    ],
    "regions": {
      "Узбекистан": [
        "Республика Каракалпакстан", "Андижанская область", "Бухарская область",
        "Джизакская область", "Кашкадарьинская область", "Навоийская область",
        "Наманганская область", "Самаркандская область", "Сурхандарьинская область",
        "Сырдарьинская область", "Ташкентская область", "Ферганская область",
        "Хорезмская область", "Город Ташкент"
      ],
      "Россия": [
        "Московская область", "Город Москва", "Ленинградская область",
        "Город Санкт-Петербург", "Краснодарский край"
      ],
      "Казахстан": [
        "Алматинская область", "Город Алматы", "Город Астана"
      ]
    }
  }
}
```

## Error Responses

### 404 Not Found
```json
{
  "success": false,
  "message": "Doctor profile not found",
  "error": "Profil topilmadi"
}
```

### 400 Bad Request
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "field_name": ["This field is required."]
  }
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Error updating profile",
  "error": "Database connection error"
}
```

## Frontend Integration Examples

### React/Next.js Example

#### Profile Page Component
```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

const DoctorProfilePage = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await axios.get('/api/doctors/profile/page/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error fetching profile');
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (formData) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await axios.patch('/api/doctors/profile/page/', formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data.data);
      return { success: true };
    } catch (err) {
      return { 
        success: false, 
        error: err.response?.data?.errors || 'Error updating profile' 
      };
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>No profile found</div>;

  return (
    <div>
      <h1>{profile.full_name}</h1>
      <p>Email: {profile.email}</p>
      <p>Phone: {profile.phone}</p>
      <p>Specialization: {profile.specialization}</p>
      {/* More profile fields */}
    </div>
  );
};

export default DoctorProfilePage;
```

#### Profile Options Hook
```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

const useProfileOptions = () => {
  const [options, setOptions] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOptions();
  }, []);

  const fetchOptions = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await axios.get('/api/doctors/profile/options/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOptions(response.data.data);
    } catch (err) {
      console.error('Error fetching options:', err);
    } finally {
      setLoading(false);
    }
  };

  return { options, loading };
};

export default useProfileOptions;
```

## Field Mapping

### Frontend to Backend Field Mapping

| Frontend Field | Backend Field | Type | Notes |
|----------------|---------------|------|-------|
| `fullName` | `user.first_name` + `user.last_name` | String | Automatically split into first/last name |
| `email` | `user.email` | Email | User model field |
| `phone` | `user.phone_number` | String | User model field |
| `specialization` | `specializations` | Array | Stored as JSON array |
| `experience` | `experience` | String | Free text field |
| `education` | `education` | Text | Free text field |
| `bio` | `bio` | Text | Free text field |
| `languages` | `languages_spoken` | Array | Stored as JSON array |
| `certifications` | `certifications` | Text | Free text field |
| `dateOfBirth` | `date_of_birth` | Date | Date field |
| `gender` | `gender` | Choice | From GENDER_CHOICES |
| `address` | `address` | Text | Free text field |
| `country` | `country` | String | Free text field |
| `region` | `region` | String | Free text field |
| `district` | `district` | String | Free text field |
| `emergencyContact` | `emergency_contact` | String | Free text field |
| `medicalLicense` | `medical_license` | String | Free text field |
| `insurance` | `insurance` | Text | Free text field |
| `workingHours` | `working_hours` | String | Free text field |
| `consultationFee` | `consultation_fee` | Decimal | Converted from string |
| `availability` | `availability` | String | Free text field |

## Notes

1. **Authentication**: Barcha endpointlar JWT token talab qiladi
2. **Field Validation**: Backend validation avtomatik ravishda amalga oshiriladi
3. **Data Types**: Frontend string formatda yuborilgan ma'lumotlar backendda to'g'ri formatga o'tkaziladi
4. **Error Handling**: Barcha xatolar standart formatda qaytariladi
5. **Success Responses**: Barcha muvaffaqiyatli javoblar `success: true` bilan boshlanadi

## Testing

API endpointlarni test qilish uchun Postman yoki boshqa API testing tool ishlatishingiz mumkin:

1. **Authentication**: JWT token olish
2. **GET Requests**: Profile ma'lumotlarini olish
3. **PATCH Requests**: Profile yangilash
4. **Error Cases**: Noto'g'ri ma'lumotlar bilan test qilish
