from django.test import TestCase
from datetime import date, time
from .models import RendezVous
from doctors.models import Medecin, Specialite
from accounts.models import CustomUser

class TestRendezVous(TestCase):

    def setUp(self):
        self.specialite = Specialite.objects.create(nom='Cardiologie')
        self.patient = CustomUser.objects.create_user(
            username='patient_test', password='test1234', role='patient'
        )
        self.user_medecin = CustomUser.objects.create_user(
            username='medecin_test', password='test1234', role='medecin'
        )
        self.medecin = Medecin.objects.create(
            user=self.user_medecin,
            specialite=self.specialite,
            est_actif=True
        )
        self.rdv = RendezVous.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            specialite=self.specialite,
            date=date.today(),
            heure=time(10, 0),
            motif='Test consultation',
            statut='en_attente'
        )

    def test_rdv_cree(self):
        self.assertEqual(RendezVous.objects.count(), 1)

    def test_rdv_statut_initial(self):
        self.assertEqual(self.rdv.statut, 'en_attente')

    def test_annuler_rdv(self):
        self.rdv.statut = 'annule'
        self.rdv.save()
        self.rdv.refresh_from_db()
        self.assertEqual(self.rdv.statut, 'annule')

    def test_rdv_patient(self):
        self.assertEqual(self.rdv.patient.username, 'patient_test')

    def test_rdv_medecin(self):
        self.assertEqual(self.rdv.medecin, self.medecin)

    def test_mes_rdv_redirige_si_non_connecte(self):
        response = self.client.get('/appointments/mes-rdv/')
        self.assertEqual(response.status_code, 302)