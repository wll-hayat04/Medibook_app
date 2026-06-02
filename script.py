import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medibook_project.settings')
django.setup()

from accounts.models import CustomUser
from doctors.models import Medecin, Specialite
from schedules.models import Disponibilite
from datetime import time

# Spécialités
specs = ['Cardiologie', 'Dermatologie', 'Pédiatrie', 'Gynécologie', 'Ophtalmologie', 'Dentisterie', 'Neurologie', 'Médecine générale']
for s in specs:
    Specialite.objects.get_or_create(nom=s)
print("✅ Spécialités créées")

# Médecins
medecins_data = [
    ('dr.benali', 'Hassan', 'Benali', 'Cardiologie', '+212 537-201-001', '12 Avenue Mohammed V, Rabat', 'Cardiologue expérimenté spécialisé dans les maladies cardiovasculaires.', 15),
    ('dr.alami', 'Fatima', 'Alami', 'Pédiatrie', '+212 537-202-002', '34 Rue Ibn Khaldoun, Rabat', 'Pédiatre dévouée spécialisée dans le suivi de la croissance.', 12),
    ('dr.idrissi', 'Youssef', 'Idrissi', 'Neurologie', '+212 537-203-003', '5 Boulevard Hassan II, Salé', 'Neurologue spécialisé dans les migraines et épilepsies.', 18),
    ('dr.tazi', 'Nadia', 'Tazi', 'Dermatologie', '+212 537-204-004', '78 Rue Patrice Lumumba, Rabat', 'Dermatologue spécialisée dans acné, eczéma et psoriasis.', 10),
    ('dr.chraibi', 'Karim', 'Chraibi', 'Ophtalmologie', '+212 537-205-005', '23 Avenue Fal Ould Oumeir, Agdal', 'Ophtalmologue expert en chirurgie de la cataracte.', 20),
    ('dr.mansouri', 'Sara', 'Mansouri', 'Gynécologie', '+212 537-206-006', '15 Rue Oued Fès, Agdal, Rabat', 'Gynécologue obstétricienne spécialisée en suivi de grossesse.', 14),
    ('dr.elfassi', 'Omar', 'El Fassi', 'Dentisterie', '+212 537-207-007', '9 Avenue Annakhil, Hay Riad', 'Chirurgien dentiste spécialisé en implantologie et orthodontie.', 8),
    ('dr.benkiran', 'Leila', 'Benkiran', 'Médecine générale', '+212 537-208-008', '45 Rue Mohamed Diouri, Centre ville', 'Médecin généraliste pour consultations et bilans de santé.', 7),
]

for username, prenom, nom, spec, tel, adresse, desc, exp in medecins_data:
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
    Medecin.objects.get_or_create(
        user=user,
        defaults={
            'specialite': specialite,
            'telephone_professionnel': tel,
            'adresse_cabinet': adresse,
            'description': desc,
            'annees_experience': exp,
            'est_actif': True
        }
    )
print("✅ Médecins créés")

# Disponibilités
dispos = [
    ('dr.benali', 0, '09:00', '17:00', 30),
    ('dr.benali', 2, '09:00', '13:00', 30),
    ('dr.alami', 1, '08:00', '16:00', 20),
    ('dr.alami', 3, '08:00', '12:00', 20),
    ('dr.idrissi', 0, '10:00', '18:00', 45),
    ('dr.tazi', 2, '09:00', '17:00', 30),
    ('dr.chraibi', 3, '08:00', '15:00', 30),
    ('dr.mansouri', 0, '09:00', '16:00', 30),
    ('dr.elfassi', 1, '09:00', '18:00', 30),
    ('dr.benkiran', 0, '08:00', '20:00', 15),
    ('dr.benkiran', 2, '08:00', '20:00', 15),
    ('dr.benkiran', 4, '08:00', '20:00', 15),
]

for username, jour, debut, fin, duree in dispos:
    user = CustomUser.objects.get(username=username)
    medecin = Medecin.objects.get(user=user)
    h_debut = time(int(debut.split(':')[0]), int(debut.split(':')[1]))
    h_fin = time(int(fin.split(':')[0]), int(fin.split(':')[1]))
    Disponibilite.objects.get_or_create(
        medecin=medecin,
        jour=jour,
        defaults={
            'heure_debut': h_debut,
            'heure_fin': h_fin,
            'duree_rdv': duree,
            'est_actif': True
        }
    )
print("✅ Disponibilités créées")
print("🎉 TOUT EST PRÊT !")