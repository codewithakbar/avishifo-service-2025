from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView

# Simple CORS test endpoint
@csrf_exempt
def cors_test(request):
    response = JsonResponse({
        "status": "success", 
        "message": "CORS is working properly",
        "origin": request.META.get('HTTP_ORIGIN', 'No origin header'),
        "method": request.method
    })
    # Set CORS headers
    response["Access-Control-Allow-Origin"] = "https://dashboard.avishifo.uz"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

# API Router
router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CORS test endpoint
    path('api/cors-test/', cors_test, name='cors-test'),
    
    # Authentication URLs
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/medical-records/', include('medical_records.urls')),
    path('api/hospitals/', include('hospitals.urls')),
    
    # API Root
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='index.html')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
