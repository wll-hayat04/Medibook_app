from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_orientation, name='ai_orientation'),
    path('chatbot/', views.chatbot, name='chatbot'),
]