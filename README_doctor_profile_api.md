# Doctor Profile API - Frontend Integration

Bu hujjat doctor profile sahifasi uchun yaratilgan yangi API endpointlarni tavsiflaydi.

## 🚀 Yangi API Endpointlar

### 1. Profile Page Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/doctors/profile/page/` | GET | Profile sahifasini ko'rish | Required |
| `/api/doctors/profile/page/` | PATCH | Profile yangilash | Required |
| `/api/doctors/profile/stats/` | GET | Profile statistikalarini olish | Required |
| `/api/doctors/profile/fields-info/` | GET | Profile fieldlari haqida ma'lumot | Required |
| `/api/doctors/profile/options/` | GET | Profile optionlari (tillar, soatlar, mamlakatlar) | Required |

### 2. Mavjud Endpointlar

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/doctors/specialties/` | GET | Barcha ixtisosliklar ro'yxati | Not Required |
| `/api/doctors/specialties/stats/` | GET | Ixtisosliklar statistikasi | Not Required |
| `/api/doctors/specialties/choices/` | GET | Ixtisoslik tanlovlari | Not Required |

## 🔧 Model Yangilanishlari

Doctor modeliga quyidagi yangi fieldlar qo'shildi:

### Shaxsiy ma'lumotlar
- `date_of_birth` - Tug'ilgan sana
- `address` - To'liq manzil
- `country` - Mamlakat
- `region` - Viloyat/Region
- `district` - Tuman

### Kontakt ma'lumotlari
- `emergency_contact` - Favqulodda kontakt
- `medical_license` - Tibbiy litsenziya
- `insurance` - Sug'urta ma'lumoti

### Ish jadvali
- `working_hours` - Ish soatlari
- `availability` - Mavjudlik

### Statistika
- `total_patients` - Jami bemorlar
- `monthly_consultations` - Oylik maslahatlar
- `total_reviews` - Jami sharhlar
- `completed_treatments` - Tugatilgan davolanishlar
- `active_patients` - Faol bemorlar
- `monthly_income` - Oylik daromad
- `research_papers` - Ilmiy ishlar
- `conferences_attended` - Qatnashgan konferensiyalar
- `awards` - Mukofotlar

## 📱 Frontend Integration

### 1. Profile sahifasini yuklash

```javascript
const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('accessToken');
    const response = await axios.get('/api/doctors/profile/page/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    if (response.data.success) {
      setProfile(response.data.data);
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};
```

### 2. Profile yangilash

```javascript
const updateProfile = async (formData) => {
  try {
    const token = localStorage.getItem('accessToken');
    const response = await axios.patch('/api/doctors/profile/page/', formData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    if (response.data.success) {
      setProfile(response.data.data);
      showSuccessMessage('Profile muvaffaqiyatli yangilandi');
    }
  } catch (error) {
    showErrorMessage('Profile yangilashda xatolik yuz berdi');
  }
};
```

### 3. Profile optionlarini olish

```javascript
const fetchOptions = async () => {
  try {
    const token = localStorage.getItem('accessToken');
    const response = await axios.get('/api/doctors/profile/options/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    if (response.data.success) {
      setOptions(response.data.data);
    }
  } catch (error) {
    console.error('Error fetching options:', error);
  }
};
```

## 🔄 Field Mapping

Frontend va Backend o'rtasidagi field mapping:

| Frontend | Backend | Izoh |
|----------|---------|------|
| `fullName` | `user.first_name + user.last_name` | Avtomatik ajratiladi |
| `email` | `user.email` | User model field |
| `phone` | `user.phone_number` | User model field |
| `specialization` | `specializations` | JSON array sifatida saqlanadi |
| `languages` | `languages_spoken` | JSON array sifatida saqlanadi |
| `consultationFee` | `consultation_fee` | String dan decimal ga o'tkaziladi |

## 📋 API Response Format

Barcha API javoblari quyidagi formatda:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data
  }
}
```

Xatolik holatida:

```json
{
  "success": false,
  "message": "Error message",
  "error": "Detailed error information"
}
```

## 🧪 Testing

API endpointlarni test qilish uchun:

```bash
# Test scriptini ishga tushirish
python scripts/test_doctor_profile_api.py

# Yoki Postman bilan test qilish
```

## 📚 Qo'shimcha Ma'lumot

- **API Documentation**: `docs/doctor_profile_api_guide.md`
- **Models**: `doctors/models.py`
- **Views**: `doctors/views.py`
- **Serializers**: `doctors/serializers.py`
- **URLs**: `doctors/urls.py`

## 🔐 Authentication

Barcha profile endpointlari JWT token talab qiladi:

```javascript
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

## 🚨 Xatoliklar

Keng tarqalgan HTTP status kodlari:

- `200` - Muvaffaqiyatli
- `400` - Noto'g'ri ma'lumotlar
- `401` - Authentication talab qilinadi
- `404` - Profile topilmadi
- `500` - Server xatosi

## 📞 Yordam

Savollar yoki muammolar bo'lsa:
1. API dokumentatsiyasini tekshiring
2. Test scriptini ishga tushiring
3. Django server loglarini ko'ring
4. Model va serializer kodlarini tekshiring
