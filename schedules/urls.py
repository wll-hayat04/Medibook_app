from django.urls import path
from . import views

urlpatterns = [
    path('disponibilites/', views.gerer_disponibilites, name='gerer_disponibilites'),
]
