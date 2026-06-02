from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medecin, Specialite, Avis
from django.shortcuts import render, redirect
from .forms import MedecinSignUpForm
from django.contrib.auth import get_user_model
from .forms import MedecinSignUpForm

User = get_user_model()


def liste_medecins(request):
    specialite_id = request.GET.get('specialite')
    recherche = request.GET.get('q')
    experience_min = request.GET.get('experience', 0)
    medecins = Medecin.objects.all()

    if specialite_id:
        medecins = medecins.filter(specialite_id=specialite_id)
    if recherche:
        medecins = medecins.filter(
            user__first_name__icontains=recherche
        ) | medecins.filter(
            user__last_name__icontains=recherche
        )
    if experience_min:
        medecins = medecins.filter(annees_experience__gte=experience_min)

    specialites = Specialite.objects.all()
    return render(request, 'doctors/liste.html', {
        'medecins': medecins,
        'specialites': specialites,
        'recherche': recherche,
        'experience_min': experience_min,
    })

def detail_medecin(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    avis_list = Avis.objects.filter(medecin=medecin)
    moyenne = 0
    if avis_list:
        moyenne = sum(a.note for a in avis_list) / len(avis_list)
    
    user_avis = None
    if request.user.is_authenticated:
        user_avis = Avis.objects.filter(
            medecin=medecin, patient=request.user
        ).first()

    return render(request, 'doctors/detail.html', {
        'medecin': medecin,
        'avis_list': avis_list,
        'moyenne': round(moyenne, 1),
        'user_avis': user_avis,
    })

@login_required
def ajouter_avis(request, medecin_id):
    medecin = get_object_or_404(Medecin, pk=medecin_id)
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        if note and commentaire:
            Avis.objects.update_or_create(
                patient=request.user,
                medecin=medecin,
                defaults={'note': note, 'commentaire': commentaire}
            )
            messages.success(request, 'Votre avis a été publié !')
    return redirect('detail_medecin', pk=medecin_id)


@login_required
def profil_medecin(request):
    if not request.user.is_medecin():
        return redirect('accueil')
    try:
        medecin = request.user.medecin_doctors
    except:
        messages.error(request, 'Profil médecin introuvable.')
        return redirect('accueil')

    if request.method == 'POST':
        medecin.telephone_professionnel = request.POST.get('telephone', '')
        medecin.adresse_cabinet = request.POST.get('adresse', '')
        medecin.description = request.POST.get('description', '')
        medecin.annees_experience = request.POST.get('experience', 0)
        if request.FILES.get('photo'):
            medecin.photo = request.FILES['photo']
        medecin.save()

        request.user.first_name = request.POST.get('prenom', request.user.first_name)
        request.user.last_name = request.POST.get('nom', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        messages.success(request, 'Profil mis à jour !')
        return redirect('profil_medecin')

    specialites = Specialite.objects.all()
    return render(request, 'doctors/profil_medecin.html', {
        'medecin': medecin,
        'specialites': specialites,
    })
    
def medecin_signup(request):
    if request.method == 'POST':
        form = MedecinSignUpForm(request.POST)
        if form.is_valid():
            form.save()  # ça suffit
            return redirect('dashboard')  # ou page d'accueil médecin
    else:
        form = MedecinSignUpForm()
    return render(request, 'doctors/signup.html', {'form': form})

def liste_medecins_view(request):
    medecins = Medecin.objects.all()
    specialites = Specialite.objects.all()
    return render(request, 'doctors/liste.html', {
        'medecins': medecins,
        'specialites': specialites
    })
