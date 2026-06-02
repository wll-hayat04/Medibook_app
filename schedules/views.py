from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disponibilite

@login_required
def gerer_disponibilites(request):
    try:
        medecin = request.user.medecin_doctors
    except:
        return redirect('accueil')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'ajouter':
            jour = request.POST.get('jour')
            heure_debut = request.POST.get('heure_debut')
            heure_fin = request.POST.get('heure_fin')
            duree_rdv = request.POST.get('duree_rdv', 30)
            Disponibilite.objects.create(
                medecin=medecin,
                jour=jour,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                duree_rdv=duree_rdv
            )
            messages.success(request, 'Disponibilite ajoutee !')
        
        elif action == 'supprimer':
            dispo_id = request.POST.get('dispo_id')
            Disponibilite.objects.filter(id=dispo_id, medecin=medecin).delete()
            messages.success(request, 'Disponibilite supprimee !')
        
        return redirect('gerer_disponibilites')
    
    disponibilites = Disponibilite.objects.filter(medecin=medecin).order_by('jour', 'heure_debut')
    jours = Disponibilite.JOURS
    
    return render(request, 'schedules/disponibilites.html', {
        'disponibilites': disponibilites,
        'jours': jours,
        'medecin': medecin,
    })
