from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from patients.models import ProfilPatient

def accueil(request):
    return render(request, 'accueil.html')

def inscription(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'accounts/inscription.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return render(request, 'accounts/inscription.html')

        user = CustomUser.objects.create_user(
            username=username, email=email,
            password=password1, first_name=prenom,
            last_name=nom, role='patient'
        )
        ProfilPatient.objects.create(user=user)
        login(request, user)
        messages.success(request, 'Compte créé avec succès !')
        return redirect('dashboard_patient')

    return render(request, 'accounts/inscription.html')


def inscription_medecin(request):
    from doctors.models import Medecin
    from ai_orientation.models import Specialite
    specialites = Specialite.objects.all()
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        telephone = request.POST.get('telephone')
        specialite_id = request.POST.get('specialite')
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'accounts/inscription_medecin.html', {'specialites': specialites})
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d utilisateur existe deja.")
            return render(request, 'accounts/inscription_medecin.html', {'specialites': specialites})
        user = CustomUser.objects.create_user(
            username=username, email=email,
            password=password1, first_name=prenom,
            last_name=nom, role='medecin'
        )
        specialite = Specialite.objects.get(id=specialite_id)
        Medecin.objects.create(user=user, specialite=specialite, telephone=telephone)
        login(request, user)
        messages.success(request, 'Compte medecin cree avec succes !')
        return redirect('dashboard_medecin')
    return render(request, 'accounts/inscription_medecin.html', {'specialites': specialites})

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role_choisi = request.POST.get('role_choisi', 'patient')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.role != role_choisi and not user.is_superuser:
                messages.error(request, f'Ce compte n\'est pas un compte {role_choisi}.')
                return render(request, 'accounts/connexion.html')
            login(request, user)
            if user.is_medecin():
                return redirect('dashboard_medecin')
            elif user.is_admin() or user.is_superuser:
                return redirect('dashboard_admin')
            else:
                return redirect('dashboard_patient')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'accounts/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('accueil')

@login_required
def profil(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('prenom', request.user.first_name)
        request.user.last_name = request.POST.get('nom', request.user.last_name)
        request.user.telephone = request.POST.get('telephone', request.user.telephone)
        request.user.save()
        messages.success(request, 'Profil mis à jour.')
        return redirect('profil')
    return render(request, 'accounts/profil.html')
@login_required
def profil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('prenom', user.first_name)
        user.last_name = request.POST.get('nom', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.telephone = request.POST.get('telephone', user.telephone)
        if request.FILES.get('photo'):
            user.photo = request.FILES['photo']
        user.save()

        if user.is_patient():
            from patients.models import ProfilPatient
            profil_patient, _ = ProfilPatient.objects.get_or_create(user=user)
            profil_patient.date_naissance = request.POST.get('date_naissance') or None
            profil_patient.adresse = request.POST.get('adresse', '')
            profil_patient.groupe_sanguin = request.POST.get('groupe_sanguin', '')
            profil_patient.save()

        messages.success(request, 'Profil mis à jour avec succès !')
        return redirect('profil')

    profil_patient = None
    if request.user.is_patient():
        from patients.models import ProfilPatient
        profil_patient, _ = ProfilPatient.objects.get_or_create(user=request.user)

    return render(request, 'accounts/profil.html', {
        'profil_patient': profil_patient
    })

def page_404(request, exception):
    return render(request, '404.html', status=404)

def page_500(request):
    return render(request, '500.html', status=500)

def a_propos(request):
    return render(request, 'pages/a_propos.html')

def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message_text = request.POST.get('message')
        messages.success(request, f'Merci {nom} ! Votre message a été envoyé avec succès.')
        return redirect('contact')
    return render(request, 'pages/contact.html')