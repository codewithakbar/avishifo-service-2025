from django.urls import path, include
from .views import (
    KasallikTarixiAPIView, PatientCreateAPIView, PatientListAPIView, PatientListView, PatientDetailView, PatientCreateView, PatientRetrieveAPIView,
    PatientUpdateAPIView, PatientDeleteAPIView, PatientArchiveAPIView, patient_medical_summary
)
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, MedicalRecordViewSet,
    MedicalHistoryItemViewSet, PrescribedMedicationViewSet,
    VitalSignViewSet, PatientDocumentViewSet
)


router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'medical-records', MedicalRecordViewSet, basename='medicalrecord')

# Роутеры для отдельных элементов медкарты
# Это более простой способ, если не используется вложенный роутинг
router.register(r'history-items', MedicalHistoryItemViewSet, basename='medicalhistoryitem')
router.register(r'prescriptions', PrescribedMedicationViewSet, basename='prescribedmedication')
router.register(r'vital-signs', VitalSignViewSet, basename='vitalsign')
router.register(r'documents', PatientDocumentViewSet, basename='patientdocument')


# Пример для вложенного роутинга (если нужно /medical-records/{id}/history-items/)
# from rest_framework_nested import routers
# medical_record_router = routers.NestedSimpleRouter(router, r'medical-records', lookup='medical_record')
# medical_record_router.register(r'history-items', MedicalHistoryItemViewSet, basename='medicalrecord-historyitems')
# ... и так далее для других вложенных ресурсов



urlpatterns = [
    path('', include(router.urls)),
    path('', PatientListView.as_view(), name='patient-list'),

    path('create/', PatientCreateAPIView.as_view(), name='patient-create'),
    path('patientlar/', PatientListAPIView.as_view(), name='patient-list'),
    path('patientlar/<str:id>/', PatientRetrieveAPIView.as_view(), name='patient-detail'),
    path('patientlar/<str:id>/update/', PatientUpdateAPIView.as_view(), name='patient-update'),
    path('patientlar/<str:id>/delete/', PatientDeleteAPIView.as_view(), name='patient-delete'),
    path('patientlar/<str:id>/archive/', PatientArchiveAPIView.as_view(), name='patient-archive'),

    path('kasallik-tarixi/', KasallikTarixiAPIView.as_view(), name='kasallik-tarixi'),
    path('kasallik-tarixi/<int:pk>/', KasallikTarixiAPIView.as_view(), name='kasalliktarixi-update'),


    # path('create/', PatientCreateView.as_view(), name='patient-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<int:pk>/medical-summary/', patient_medical_summary, name='patient-medical-summary'),
]
