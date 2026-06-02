from django.urls import path
from . import views

urlpatterns = [
    path('patient/', views.dashboard_patient, name='dashboard_patient'),
    path('medecin/', views.dashboard_medecin, name='dashboard_medecin'),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),
]