from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from appointments.models import RendezVous
from doctors.models import Medecin, Specialite
from accounts.models import CustomUser
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from appointments.models import RendezVous
from doctors.models import Medecin, Specialite
from accounts.models import CustomUser
from datetime import date
import json

@login_required
def dashboard_patient(request):
    rdv_a_venir = RendezVous.objects.filter(
        patient=request.user,
        date__gte=date.today(),
        statut__in=['en_attente', 'confirme']
    ).order_by('date', 'heure')[:5]

    rdv_passes = RendezVous.objects.filter(
        patient=request.user,
        date__lt=date.today()
    ).order_by('-date')[:5]

    rdv_annules = RendezVous.objects.filter(
        patient=request.user,
        statut='annule'
    ).count()

    return render(request, 'dashboard/patient.html', {
        'rdv_a_venir': rdv_a_venir,
        'rdv_passes': rdv_passes,
        'rdv_annules': rdv_annules,
        'total_rdv': RendezVous.objects.filter(patient=request.user).count(),
    })

@login_required
def dashboard_medecin(request):
    if not request.user.is_medecin():
        from django.shortcuts import redirect
        return redirect('accueil')
    try:
        medecin = request.user.medecin_doctors
    except:
        from django.shortcuts import redirect
        return redirect('accueil')

    aujourd_hui = date.today()
    rdv_aujourd_hui = RendezVous.objects.filter(
        medecin=medecin, date=aujourd_hui
    ).order_by('heure')

    rdv_confirmes = RendezVous.objects.filter(
        medecin=medecin, statut='confirme'
    ).count()

    rdv_en_attente = RendezVous.objects.filter(
        medecin=medecin, statut='en_attente'
    ).count()

    total_rdv = RendezVous.objects.filter(medecin=medecin).count()

    return render(request, 'dashboard/medecin.html', {
        'rdv_aujourd_hui': rdv_aujourd_hui,
        'rdv_confirmes': rdv_confirmes,
        'rdv_en_attente': rdv_en_attente,
        'total_rdv': total_rdv,
        'medecin': medecin,
    })

@login_required
def dashboard_admin(request):
    if not request.user.is_admin():
        from django.shortcuts import redirect
        return redirect('accueil')

    total_patients = CustomUser.objects.filter(role='patient').count()
    total_medecins = CustomUser.objects.filter(role='medecin').count()
    total_rdv = RendezVous.objects.count()

    rdv_par_statut = {
        'en_attente': RendezVous.objects.filter(statut='en_attente').count(),
        'confirme': RendezVous.objects.filter(statut='confirme').count(),
        'annule': RendezVous.objects.filter(statut='annule').count(),
        'termine': RendezVous.objects.filter(statut='termine').count(),
    }

    specialites = Specialite.objects.all()
    rdv_par_specialite = []
    for s in specialites:
        count = RendezVous.objects.filter(specialite=s).count()
        rdv_par_specialite.append({'specialite': s.nom, 'count': count})

    return render(request, 'dashboard/admin.html', {
        'total_patients': total_patients,
        'total_medecins': total_medecins,
        'total_rdv': total_rdv,
        'rdv_par_statut': rdv_par_statut,
        'rdv_par_specialite': rdv_par_specialite,
    })



@login_required
def dashboard_patient(request):
    rdv_a_venir = RendezVous.objects.filter(
        patient=request.user,
        date__gte=date.today(),
        statut__in=['en_attente', 'confirme']
    ).order_by('date', 'heure')[:5]

    rdv_passes = RendezVous.objects.filter(
        patient=request.user,
        date__lt=date.today()
    ).order_by('-date')[:5]

    rdv_annules = RendezVous.objects.filter(
        patient=request.user, statut='annule'
    ).count()

    total_rdv = RendezVous.objects.filter(patient=request.user).count()

    # Données pour graphique
    statuts = {
        'En attente': RendezVous.objects.filter(patient=request.user, statut='en_attente').count(),
        'Confirmés': RendezVous.objects.filter(patient=request.user, statut='confirme').count(),
        'Annulés': rdv_annules,
        'Terminés': RendezVous.objects.filter(patient=request.user, statut='termine').count(),
    }

    return render(request, 'dashboard/patient.html', {
        'rdv_a_venir': rdv_a_venir,
        'rdv_passes': rdv_passes,
        'rdv_annules': rdv_annules,
        'total_rdv': total_rdv,
        'statuts_json': json.dumps(statuts),
    })

@login_required
def dashboard_medecin(request):
    if not request.user.is_medecin():
        return redirect('accueil')
    try:
        medecin = request.user.medecin_doctors
    except:
        return redirect('accueil')

    aujourd_hui = date.today()
    rdv_aujourd_hui = RendezVous.objects.filter(
        medecin=medecin, date=aujourd_hui
    ).order_by('heure')

    rdv_confirmes = RendezVous.objects.filter(medecin=medecin, statut='confirme').count()
    rdv_en_attente = RendezVous.objects.filter(medecin=medecin, statut='en_attente').count()
    total_rdv = RendezVous.objects.filter(medecin=medecin).count()

    # Données graphique
    statuts = {
        'En attente': rdv_en_attente,
        'Confirmés': rdv_confirmes,
        'Annulés': RendezVous.objects.filter(medecin=medecin, statut='annule').count(),
        'Terminés': RendezVous.objects.filter(medecin=medecin, statut='termine').count(),
    }

    return render(request, 'dashboard/medecin.html', {
        'rdv_aujourd_hui': rdv_aujourd_hui,
        'rdv_confirmes': rdv_confirmes,
        'rdv_en_attente': rdv_en_attente,
        'total_rdv': total_rdv,
        'medecin': medecin,
        'statuts_json': json.dumps(statuts),
    })

@login_required
def dashboard_admin(request):
    if not request.user.is_admin():
        return redirect('accueil')

    from datetime import date, timedelta
    from django.db.models import Count

    total_patients = CustomUser.objects.filter(role='patient').count()
    total_medecins = CustomUser.objects.filter(role='medecin').count()
    total_rdv = RendezVous.objects.count()
    rdv_aujourd_hui = RendezVous.objects.filter(date=date.today()).count()

    rdv_par_statut = {
        'En attente': RendezVous.objects.filter(statut='en_attente').count(),
        'Confirmés': RendezVous.objects.filter(statut='confirme').count(),
        'Annulés': RendezVous.objects.filter(statut='annule').count(),
        'Terminés': RendezVous.objects.filter(statut='termine').count(),
    }

    specialites = Specialite.objects.all()
    rdv_par_specialite = {
        s.nom: RendezVous.objects.filter(specialite=s).count()
        for s in specialites
    }

    # Top médecins
    top_medecins = Medecin.objects.annotate(
        nb_rdv=Count('rendez_vous')
    ).order_by('-nb_rdv')[:5]

    # RDV des 7 derniers jours
    rdv_semaine = {}
    for i in range(6, -1, -1):
        jour = date.today() - timedelta(days=i)
        rdv_semaine[jour.strftime('%d/%m')] = RendezVous.objects.filter(date=jour).count()

    return render(request, 'dashboard/admin.html', {
        'total_patients': total_patients,
        'total_medecins': total_medecins,
        'total_rdv': total_rdv,
        'rdv_aujourd_hui': rdv_aujourd_hui,
        'rdv_par_statut': rdv_par_statut,
        'rdv_par_statut_json': json.dumps(rdv_par_statut),
        'rdv_par_specialite_json': json.dumps(rdv_par_specialite),
        'top_medecins': top_medecins,
        'rdv_semaine_json': json.dumps(rdv_semaine),
    })