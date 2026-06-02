import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medibook_project.settings')
django.setup()

from accounts.models import CustomUser
from doctors.models import Medecin, Specialite
from schedules.models import Disponibilite
from datetime import time

medecins_data = [
    ('dr.berrada',     'Amine',   'Berrada',     'Médecine générale',
     'Médecin généraliste assurant le suivi médical global des patients.'),
    ('dr.elmansouri',  'Youssef', 'El Mansouri', 'Cardiologie',
     'Spécialiste des maladies du cœur et du système cardiovasculaire.'),
    ('dr.elidrissi',   'Salma',   'El Idrissi',  'Dermatologie',
     'Spécialiste des maladies de la peau, des cheveux et des ongles.'),
    ('dr.lbennani',    'Leila',   'Bennani',     'Pédiatrie',
     'Spécialiste du suivi médical des enfants et adolescents.'),
    ('dr.alaoui',      'Nadia',   'Alaoui',      'Gynécologie',
     'Spécialiste de la santé de la femme et du suivi gynécologique.'),
    ('dr.ktazi',       'Karim',   'Tazi',        'Ophtalmologie',
     'Spécialiste des troubles de la vision et des maladies des yeux.'),
    ('dr.rachidi',     'Mehdi',   'Rachidi',     'Dentisterie',
     'Spécialiste des soins dentaires et bucco-dentaires.'),
    ('dr.lahlou',      'Samir',   'Lahlou',      'ORL',
     'Spécialiste des maladies de l\'oreille, du nez et de la gorge.'),
    ('dr.naciri',      'Hicham',  'Naciri',      'Neurologie',
     'Spécialiste des troubles du système nerveux.'),
    ('dr.amrani',      'Sara',    'Amrani',      'Radiologie',
     'Spécialiste de l\'imagerie médicale et de l\'interprétation radiologique.'),
    ('dr.ochraibi',    'Omar',    'Chraibi',     'Orthopédie',
     'Spécialiste des os, des articulations et de l\'appareil locomoteur.'),
    ('dr.kettani',     'Imane',   'Kettani',     'Néphrologie',
     'Spécialiste des maladies des reins et du suivi rénal.'),
    ('dr.fassi',       'Rania',   'Fassi',       'Hématologie',
     'Spécialiste des maladies du sang.'),
    ('dr.elfassi',     'Anas',    'El Fassi',    'Psychiatrie',
     'Spécialiste de la santé mentale et des troubles psychiques.'),
    ('dr.laghzaoui',   'Mariam',  'Laghzaoui',  'Endocrinologie',
     'Spécialiste des troubles hormonaux et métaboliques.'),
]

# Spécialités à créer si elles n'existent pas
specialites_new = [
    'ORL', 'Radiologie', 'Orthopédie',
    'Néphrologie', 'Hématologie', 'Psychiatrie', 'Endocrinologie'
]
for s in specialites_new:
    Specialite.objects.get_or_create(nom=s)
print("✅ Spécialités vérifiées")

# Créer les médecins
for username, prenom, nom, spec, desc in medecins_data:
    user, created = CustomUser.objects.get_or_create(
        username=username,
        defaults={
            'first_name': prenom,
            'last_name': nom,
            'email': f'{username}@medibook.ma',
            'role': 'medecin'
        }
    )
    if created:
        user.set_password('medecin1234')
        user.save()

    specialite = Specialite.objects.get(nom=spec)
    medecin, _ = Medecin.objects.get_or_create(
        user=user,
        defaults={
            'specialite': specialite,
            'telephone_professionnel': '+212 537-000-000',
            'adresse_cabinet': 'Rabat, Maroc',
            'description': desc,
            'annees_experience': 10,
            'est_actif': True
        }
    )
    print(f"✅ {prenom} {nom} — {spec}")

# Disponibilités : lundi +