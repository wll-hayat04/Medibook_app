from django.urls import path
from . import views
from .views import medecin_signup, liste_medecins_view

urlpatterns = [
    path('', views.liste_medecins, name='liste_medecins'),  # page par défaut
    path('signup/', medecin_signup, name='medecin_signup'),  # inscription médecin
    path('liste/', liste_medecins_view, name='liste_medecins_view'),  # liste alternative
    path('<int:pk>/', views.detail_medecin, name='detail_medecin'),  # profil médecin
    path('<int:medecin_id>/avis/', views.ajouter_avis, name='ajouter_avis'),  # avis
    path('profil/edit/', views.profil_medecin, name='profil_medecin'),  # édition profil
]