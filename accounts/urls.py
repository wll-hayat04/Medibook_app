from django.urls import path
from . import views


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/medecin/', views.inscription_medecin, name='inscription_medecin'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('contact/', views.contact, name='contact'),
]