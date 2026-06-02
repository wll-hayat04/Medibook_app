from django.urls import path
from . import views

urlpatterns = [
    path('prendre/<int:medecin_id>/', views.prendre_rdv, name='prendre_rdv'),
    path('mes-rdv/', views.mes_rdv, name='mes_rdv'),
    path('annuler/<int:rdv_id>/', views.annuler_rdv, name='annuler_rdv'),
    path('medecin/', views.rdv_medecin, name='rdv_medecin'),
    path('confirmer/<int:rdv_id>/', views.confirmer_rdv, name='confirmer_rdv'),
    path('detail/<int:rdv_id>/', views.detail_rdv, name='detail_rdv'),
    path('calendrier/', views.calendrier_rdv, name='calendrier_rdv'),
    path('modifier/<int:rdv_id>/', views.modifier_rdv, name='modifier_rdv'),
    path('consultation/<int:rdv_id>/', views.ajouter_consultation, name='ajouter_consultation'),
    path('absent/<int:rdv_id>/', views.marquer_absent, name='marquer_absent'),
    path('planning/', views.planning_medecin, name='planning_medecin'),

]