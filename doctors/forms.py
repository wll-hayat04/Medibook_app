from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from doctors.models import Medecin, Specialite

class MedecinSignUpForm(UserCreationForm):
    specialite = forms.ModelChoiceField(queryset=Specialite.objects.all(), required=True)
    telephone_professionnel = forms.CharField(max_length=20, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'specialite', 'telephone_professionnel']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_medecin = True  # flag pour identifier que c'est un médecin
        if commit:
            user.save()
            Medecin.objects.create(
                user=user,
                specialite=self.cleaned_data['specialite'],
                telephone_professionnel=self.cleaned_data['telephone_professionnel']
            )
        return user