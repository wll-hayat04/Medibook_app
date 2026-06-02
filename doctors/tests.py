from django.test import TestCase
from .models import Specialite, Medecin
from accounts.models import CustomUser

class TestDoctors(TestCase):

    def setUp(self):
        self.specialite = Specialite.objects.create(nom='Cardiologie')
        self.user_medecin = CustomUser.objects.create_user(
            username='dr.test', password='test1234',
            first_name='Hassan', last_name='Benali', role='medecin'
        )
        self.medecin = Medecin.objects.create(
            user=self.user_medecin,
            specialite=self.specialite,
            est_actif=True
        )

    def test_specialite_creee(self):
        self.assertEqual(Specialite.objects.count(), 1)
        self.assertEqual(self.specialite.nom, 'Cardiologie')

    def test_medecin_cree(self):
        self.assertEqual(Medecin.objects.count(), 1)

    def test_medecin_actif(self):
        self.assertTrue(self.medecin.est_actif)

    def test_medecin_str(self):
        self.assertIn('Benali', str(self.medecin))

    def test_medecin_specialite(self):
        self.assertEqual(self.medecin.specialite.nom, 'Cardiologie')