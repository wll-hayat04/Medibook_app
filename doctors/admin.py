from django.contrib import admin
from .models import Medecin, Specialite

admin.site.register(Specialite)
admin.site.register(Medecin)