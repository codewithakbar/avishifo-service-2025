# Doctor Profile Management API Guide

## Overview

This guide covers the comprehensive Doctor Profile Management API that handles all profile information fields shown in the UI. The API provides GET, PUT, and PATCH methods for complete profile management.

## Base URL

```
/api/doctors/
```

## Authentication

All endpoints require authentication. The doctor must be logged in to access their profile.

**Header Required:**
```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### 1. Get Doctor Profile

**Endpoint:** `GET /api/doctors/profile/`

**Description:** Retrieve complete doctor profile information

**Response:**
```json
{
    "success": true,
    "message": "Doctor profile retrieved successfully",
    "data": {
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
        "experience_text": "15 лет",
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
            "Сертификат по эхокардиографии"
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
            "linkedin": "https://linkedin.com/in/akbar-tugayevich"
        },
        "bio": "Опытный кардиолог с 15-летним стажем работы.",
        "specializations": ["echocardiography", "interventional_cardiology"],
        "gender": "male",
        "gender_label": "Мужской",
        "emergency_contact": "+998901234568",
        "insurance_info": "Принимаю все основные страховые полисы",
        "working_hours": "Понедельник - Пятница: 09:00-17:00",
        "availability_status": "Доступен для консультаций",
        "total_income": "4500000.00",
        "income_formatted": "4.5M",
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
}
```

### 2. Update Complete Doctor Profile

**Endpoint:** `PUT /api/doctors/profile/`

**Description:** Update complete doctor profile (all fields)

**Request Body:**
```json
{
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
    "online_consultation_available": true,
    "certifications": [
        "Сертификат кардиолога высшей категории - Обновлено",
        "Сертификат по эхокардиографии - Обновлено",
        "Сертификат по интервенционной кардиологии - Новый"
    ]
}
```

**Response:** Same as GET response with updated data

### 3. Partially Update Doctor Profile

**Endpoint:** `PATCH /api/doctors/profile/`

**Description:** Update specific fields in doctor profile

**Request Body (Example 1 - Personal Information):**
```json
{
    "bio": "Обновленная биография с новыми достижениями и специализациями.",
    "gender": "male",
    "languages_spoken": ["Русский", "Узбекский", "Английский", "Немецкий"]
}
```

**Request Body (Example 2 - Professional Information):**
```json
{
    "specialty": "cardiology",
    "years_of_experience": 17,
    "education": "Ташкентский медицинский институт, 2010 - Дополнительное образование",
    "certifications": [
        "Сертификат кардиолога высшей категории",
        "Сертификат по эхокардиографии",
        "Сертификат по интервенционной кардиологии",
        "Новый сертификат по профилактической кардиологии"
    ],
    "license_number": "MD123456-UPDATED"
}
```

**Request Body (Example 3 - Work Schedule):**
```json
{
    "working_hours": "Понедельник - Пятница: 09:00-19:00, Суббота: 09:00-15:00",
    "availability_status": "Доступен по предварительной записи, возможны экстренные консультации",
    "consultation_fee": "200000.00",
    "consultation_schedule": {
        "monday": "09:00-19:00",
        "tuesday": "09:00-19:00",
        "wednesday": "09:00-19:00",
        "thursday": "09:00-19:00",
        "friday": "09:00-19:00",
        "saturday": "09:00-15:00"
    }
}
```

**Request Body (Example 4 - Contact Information):**
```json
{
    "emergency_contact": "+998901234569",
    "insurance_info": "Расширенный список страховых компаний, включая международные",
    "work_email": "akbar.cardio.new@hospital.uz",
    "work_phone": "+998901234567",
    "social_media_links": {
        "linkedin": "https://linkedin.com/in/akbar-tugayevich",
        "researchgate": "https://researchgate.net/profile/akbar-tugayevich",
        "twitter": "https://twitter.com/akbar_cardio"
    }
}
```

**Response:** Same as GET response with updated data

### 4. Get Profile Fields Information

**Endpoint:** `GET /api/doctors/profile/fields/`

**Description:** Get information about all available profile fields and their types

**Response:**
```json
{
    "success": true,
    "message": "Profile fields information retrieved successfully",
    "data": {
        "personal_information": {
            "full_name": {
                "type": "string",
                "source": "user.first_name + user.last_name",
                "required": true
            },
            "email": {
                "type": "email",
                "source": "user.email",
                "required": true
            },
            "bio": {
                "type": "text",
                "source": "bio",
                "required": false
            },
            "date_of_birth": {
                "type": "date",
                "source": "user.date_of_birth",
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
            "languages_spoken": {
                "type": "json_array",
                "source": "languages_spoken",
                "required": false
            }
        },
        "professional_information": {
            "specialty": {
                "type": "choice",
                "source": "specialty",
                "required": false,
                "choices": {
                    "cardiology": "Кардиология",
                    "neurology": "Неврология",
                    "pediatrics": "Педиатрия",
                    "internal_medicine": "Терапия (внутренние болезни)",
                    "general_surgery": "Общая хирургия"
                }
            },
            "years_of_experience": {
                "type": "integer",
                "source": "years_of_experience",
                "required": false
            },
            "education": {
                "type": "text",
                "source": "education",
                "required": false
            },
            "certifications": {
                "type": "json_array",
                "source": "certifications",
                "required": false
            },
            "license_number": {
                "type": "string",
                "source": "license_number",
                "required": false
            },
            "insurance_info": {
                "type": "text",
                "source": "insurance_info",
                "required": false
            }
        },
        "work_schedule": {
            "working_hours": {
                "type": "text",
                "source": "working_hours",
                "required": false
            },
            "availability_status": {
                "type": "string",
                "source": "availability_status",
                "required": false
            },
            "consultation_fee": {
                "type": "decimal",
                "source": "consultation_fee",
                "required": false
            }
        },
        "contact_information": {
            "phone": {
                "type": "string",
                "source": "user.phone_number",
                "required": false
            },
            "emergency_contact": {
                "type": "string",
                "source": "emergency_contact",
                "required": false
            },
            "address": {
                "type": "text",
                "source": "user.address",
                "required": false
            }
        }
    }
}
```

## Profile Fields Mapping

### Personal Information (Личная информация)
| UI Field | API Field | Type | Source | Required |
|----------|-----------|------|---------|----------|
| Полное имя | full_name | string | user.first_name + user.last_name | ✅ |
| Email | email | email | user.email | ✅ |
| Биография | bio | text | bio | ❌ |
| Дата рождения | date_of_birth | date | user.date_of_birth | ❌ |
| Пол | gender | choice | gender | ❌ |
| Языки | languages_spoken | json_array | languages_spoken | ❌ |

### Professional Information (Профессиональная информация)
| UI Field | API Field | Type | Source | Required |
|----------|-----------|------|---------|----------|
| Специализация | specialty | choice | specialty | ❌ |
| Опыт работы | years_of_experience | integer | years_of_experience | ❌ |
| Образование | education | text | education | ❌ |
| Сертификаты | certifications | json_array | certifications | ❌ |
| Медицинская лицензия | license_number | string | license_number | ❌ |
| Страхование | insurance_info | text | insurance_info | ❌ |

### Work Schedule (Рабочий график)
| UI Field | API Field | Type | Source | Required |
|----------|-----------|------|---------|----------|
| Рабочие часы | working_hours | text | working_hours | ❌ |
| Доступность | availability_status | string | availability_status | ❌ |
| Стоимость консультации | consultation_fee | decimal | consultation_fee | ❌ |

### Contact Information (Контактная информация)
| UI Field | API Field | Type | Source | Required |
|----------|-----------|------|---------|----------|
| Телефон | phone_number | string | user.phone_number | ❌ |
| Экстренный контакт | emergency_contact | string | emergency_contact | ❌ |
| Адрес | address | text | user.address | ❌ |

## Field Types and Validation

### Choice Fields
- **gender**: `male`, `female`, `other`, `not_specified`
- **specialty**: All predefined medical specialties
- **category**: `first`, `higher`, `professor`, `candidate`, `doctor_science`, `no_category`
- **degree**: `none`, `phd`, `dsc`, `md`

### JSON Array Fields
- **languages_spoken**: Array of language strings
- **certifications**: Array of certification strings
- **specializations**: Array of specialization strings
- **social_media_links**: Object with platform: URL mapping

### Numeric Fields
- **years_of_experience**: Positive integer
- **consultation_fee**: Positive decimal
- **total_income**: Positive decimal
- **rating**: Decimal between 0.00 and 5.00

## Error Handling

### Common Error Responses

**400 Bad Request - Validation Error:**
```json
{
    "success": false,
    "message": "Validation error",
    "errors": {
        "consultation_fee": ["This field must be a positive number."],
        "years_of_experience": ["This field must be a positive integer."]
    }
}
```

**404 Not Found - Profile Not Found:**
```json
{
    "success": false,
    "message": "Doctor profile not found",
    "error": "Profil topilmadi"
}
```

**500 Internal Server Error:**
```json
{
    "success": false,
    "message": "Error updating profile",
    "error": "Database connection error"
}
```

## Usage Examples

### Frontend Integration

**1. Load Profile on Page Load:**
```javascript
// GET profile data
const response = await fetch('/api/doctors/profile/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
});

const profileData = await response.json();
if (profileData.success) {
    // Populate form fields
    populateForm(profileData.data);
}
```

**2. Save Complete Profile:**
```javascript
// PUT complete profile
const profileData = collectFormData();
const response = await fetch('/api/doctors/profile/', {
    method: 'PUT',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(profileData)
});

const result = await response.json();
if (result.success) {
    showSuccessMessage('Profile updated successfully');
}
```

**3. Update Specific Fields:**
```javascript
// PATCH specific fields
const updates = {
    bio: newBio,
    consultation_fee: newFee,
    working_hours: newHours
};

const response = await fetch('/api/doctors/profile/', {
    method: 'PATCH',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
});

const result = await response.json();
if (result.success) {
    showSuccessMessage('Profile partially updated');
}
```

**4. Get Field Information for Form Generation:**
```javascript
// GET field information
const response = await fetch('/api/doctors/profile/fields/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
});

const fieldsInfo = await response.json();
if (fieldsInfo.success) {
    // Generate dynamic form based on field types
    generateForm(fieldsInfo.data);
}
```

## Testing

Use the provided test script to verify all functionality:

```bash
python scripts/test_doctor_profile_api.py
```

This script demonstrates:
- Creating sample data
- Testing all API methods (GET, PUT, PATCH)
- Validating field handling
- Testing computed fields
- Error handling scenarios

## Best Practices

1. **Use PATCH for partial updates** to avoid overwriting unchanged fields
2. **Validate data on frontend** before sending to API
3. **Handle nested user data** carefully in updates
4. **Use computed fields** for UI display (e.g., `formatted_rating`, `income_formatted`)
5. **Implement proper error handling** for all API responses
6. **Cache profile data** when appropriate to reduce API calls
7. **Use field information endpoint** for dynamic form generation

## Support

For questions or issues with the Doctor Profile API:
- Check the test script: `scripts/test_doctor_profile_api.py`
- Review the main API documentation: `docs/doctor_api_documentation.md`
- Check the views implementation: `doctors/views.py`
- Verify URL configuration: `doctors/urls.py`
