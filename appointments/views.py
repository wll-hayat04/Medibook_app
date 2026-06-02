from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime, timedelta
from .models import RendezVous
from doctors.models import Medecin
from schedules.models import Disponibilite

def get_creneaux_disponibles(medecin, date_choisie):
    jour_semaine = date_choisie.weekday()
    disponibilites = Disponibilite.objects.filter(
        medecin=medecin, jour=jour_semaine, est_actif=True
    )
    creneaux = []
    for dispo in disponibilites:
        heure = datetime.combine(date_choisie, dispo.heure_debut)
        fin = datetime.combine(date_choisie, dispo.heure_fin)
        while heure < fin:
            rdv_existe = RendezVous.objects.filter(
                medecin=medecin,
                date=date_choisie,
                heure=heure.time(),
                statut__in=['en_attente', 'confirme']
            ).exists()
            if not rdv_existe:
                creneaux.append(heure.time())
            heure += timedelta(minutes=dispo.duree_rdv)
    return creneaux

from django.core.mail import send_mail
from django.template.loader import render_to_string

@login_required
def prendre_rdv(request, medecin_id):
    medecin = get_object_or_404(Medecin, pk=medecin_id)
    creneaux = []
    date_choisie = None

    if request.method == 'POST':
        date_str = request.POST.get('date')
        heure_str = request.POST.get('heure')
        motif = request.POST.get('motif')

        if date_str and heure_str and motif:
            date_choisie = datetime.strptime(date_str, '%Y-%m-%d').date()
            heure_choisie = datetime.strptime(heure_str, '%H:%M').time()

            rdv_existe = RendezVous.objects.filter(
                medecin=medecin, date=date_choisie,
                heure=heure_choisie, statut__in=['en_attente', 'confirme']
            ).exists()

            if rdv_existe:
                messages.error(request, 'Ce créneau est déjà pris.')
            else:
                rdv = RendezVous.objects.create(
                    patient=request.user,
                    medecin=medecin,
                    specialite=medecin.specialite,
                    date=date_choisie,
                    heure=heure_choisie,
                    motif=motif,
                    statut='en_attente'
                )
                # Notification en base
                from notifications.models import Notification
                Notification.objects.create(
                    utilisateur=request.user,
                    message=f"Votre RDV avec {medecin} le {date_choisie.strftime('%d/%m/%Y')} à {heure_choisie.strftime('%H:%M')} a été enregistré."
                )
                # Email de confirmation (affiché dans terminal)
                try:
                    send_mail(
                        subject='Confirmation de votre rendez-vous — MediBook',
                        message=f"""
Bonjour {request.user.first_name},

Votre rendez-vous a été enregistré avec succès.

Médecin : {medecin}
Spécialité : {medecin.specialite}
Date : {date_choisie.strftime('%d/%m/%Y')}
Heure : {heure_choisie.strftime('%H:%M')}
Motif : {motif}

Statut : En attente de confirmation

Connectez-vous sur MediBook pour gérer vos rendez-vous.

Cordialement,
L'équipe MediBook
                        """,
                        from_email='noreply@medibook.ma',
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )
                except:
                    pass

                messages.success(request, '✅ Rendez-vous pris avec succès ! Un email de confirmation vous a été envoyé.')
                return redirect('mes_rdv')

        elif date_str:
            date_choisie = datetime.strptime(date_str, '%Y-%m-%d').date()
            creneaux = get_creneaux_disponibles(medecin, date_choisie)

    return render(request, 'appointments/prendre_rdv.html', {
        'medecin': medecin,
        'creneaux': creneaux,
        'date_choisie': date_choisie,
        'aujourd_hui': date.today().strftime('%Y-%m-%d'),
    })

@login_required
def mes_rdv(request):
    rdv_list = RendezVous.objects.filter(patient=request.user).order_by('-date', '-heure')
    return render(request, 'appointments/mes_rdv.html', {'rdv_list': rdv_list})

@login_required
def annuler_rdv(request, rdv_id):
    rdv = get_object_or_404(RendezVous, pk=rdv_id, patient=request.user)
    if rdv.statut in ['en_attente', 'confirme']:
        rdv.statut = 'annule'
        rdv.save()
        messages.success(request, 'Rendez-vous annulé.')
    return redirect('mes_rdv')

@login_required
def rdv_medecin(request):
    if not request.user.is_medecin():
        return redirect('accueil')
    try:
        medecin = request.user.medecin_doctors
    except:
        messages.error(request, 'Profil médecin introuvable.')
        return redirect('accueil')
    rdv_list = RendezVous.objects.filter(medecin=medecin).order_by('-date', '-heure')
    return render(request, 'appointments/rdv_medecin.html', {'rdv_list': rdv_list})

@login_required
def confirmer_rdv(request, rdv_id):
    try:
        medecin = request.user.medecin_doctors
    except:
        return redirect('accueil')
    rdv = get_object_or_404(RendezVous, pk=rdv_id, medecin=medecin)
    rdv.statut = 'confirme'
    rdv.save()
    messages.success(request, 'Rendez-vous confirmé.')
    return redirect('rdv_medecin')


@login_required
def detail_rdv(request, rdv_id):
    rdv = get_object_or_404(RendezVous, pk=rdv_id, patient=request.user)
    return render(request, 'appointments/detail_rdv.html', {'rdv': rdv})


@login_required
def calendrier_rdv(request):
    import json
    rdv_list = RendezVous.objects.filter(patient=request.user)
    events = []
    for rdv in rdv_list:
        color = {
            'en_attente': '#f39c12',
            'confirme': '#27ae60',
            'annule': '#e74c3c',
            'termine': '#3498db',
        }.get(rdv.statut, '#95a5a6')
        events.append({
            'title': f'Dr. {rdv.medecin.user.last_name} — {rdv.heure.strftime("%H:%M")}',
            'start': f'{rdv.date}T{rdv.heure}',
            'color': color,
            'url': f'/appointments/detail/{rdv.pk}/',
        })
    return render(request, 'appointments/calendrier.html', {
        'events_json': json.dumps(events)
    })


@login_required
def modifier_rdv(request, rdv_id):
    rdv = get_object_or_404(RendezVous, pk=rdv_id, patient=request.user)
    if rdv.statut not in ['en_attente', 'confirme']:
        messages.error(request, 'Ce rendez-vous ne peut plus être modifié.')
        return redirect('mes_rdv')

    medecin = rdv.medecin
    creneaux = []
    date_choisie = None

    if request.method == 'POST':
        date_str = request.POST.get('date')
        heure_str = request.POST.get('heure')
        motif = request.POST.get('motif')

        if date_str and heure_str and motif:
            date_choisie = datetime.strptime(date_str, '%Y-%m-%d').date()
            heure_choisie = datetime.strptime(heure_str, '%H:%M').time()

            rdv_existe = RendezVous.objects.filter(
                medecin=medecin,
                date=date_choisie,
                heure=heure_choisie,
                statut__in=['en_attente', 'confirme']
            ).exclude(pk=rdv_id).exists()

            if rdv_existe:
                messages.error(request, 'Ce créneau est déjà pris.')
            else:
                rdv.date = date_choisie
                rdv.heure = heure_choisie
                rdv.motif = motif
                rdv.statut = 'en_attente'
                rdv.save()
                from notifications.models import Notification
                Notification.objects.create(
                    utilisateur=request.user,
                    message=f"Votre RDV avec {medecin} a été modifié pour le {date_choisie.strftime('%d/%m/%Y')} à {heure_choisie.strftime('%H:%M')}."
                )
                messages.success(request, 'Rendez-vous modifié avec succès !')
                return redirect('mes_rdv')

        elif date_str:
            date_choisie = datetime.strptime(date_str, '%Y-%m-%d').date()
            creneaux = get_creneaux_disponibles(medecin, date_choisie)

    return render(request, 'appointments/modifier_rdv.html', {
        'rdv': rdv,
        'medecin': medecin,
        'creneaux': creneaux,
        'date_choisie': date_choisie,
        'aujourd_hui': date.today().strftime('%Y-%m-%d'),
    })

@login_required
def ajouter_consultation(request, rdv_id):
    try:
        medecin = request.user.medecin_doctors
    except:
        return redirect('accueil')
    rdv = get_object_or_404(RendezVous, pk=rdv_id, medecin=medecin)
    if request.method == 'POST':
        resume = request.POST.get('resume', '')
        from .models import Consultation
        Consultation.objects.update_or_create(
            rendez_vous=rdv,
            defaults={'resume': resume}
        )
        rdv.statut = 'termine'
        rdv.save()
        messages.success(request, 'Consultation enregistrée avec succès !')
        return redirect('rdv_medecin')
    return render(request, 'appointments/consultation.html', {'rdv': rdv})

@login_required
def marquer_absent(request, rdv_id):
    try:
        medecin = request.user.medecin_doctors
    except:
        return redirect('accueil')
    rdv = get_object_or_404(RendezVous, pk=rdv_id, medecin=medecin)
    rdv.statut = 'absent'
    rdv.save()
    messages.success(request, 'Patient marqué absent.')
    return redirect('rdv_medecin')


@login_required
def planning_medecin(request):
    try:
        medecin = request.user.medecin_doctors
    except:
        return redirect('accueil')
    from datetime import date, timedelta
    aujourd_hui = date.today()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    jours = []
    for i in range(7):
        jour = debut_semaine + timedelta(days=i)
        rdv_jour = RendezVous.objects.filter(
            medecin=medecin,
            date=jour,
            statut__in=['en_attente', 'confirme']
        ).order_by('heure')
        jours.append({'date': jour, 'rdv': rdv_jour})
    return render(request, 'appointments/planning.html', {
        'jours': jours,
        'debut_semaine': debut_semaine,
    })