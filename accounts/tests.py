from django.test import TestCase
from .models import CustomUser
from patients.models import ProfilPatient

class TestAuthentification(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testpatient', password='test1234',
            first_name='Sofia', last_name='Test', role='patient'
        )

    def test_user_cree(self):
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_role_patient(self):
        self.assertTrue(self.user.is_patient())
        self.assertFalse(self.user.is_medecin())

    def test_user_role_medecin(self):
        medecin = CustomUser.objects.create_user(
            username='dr.test', password='test1234', role='medecin'
        )
        self.assertTrue(medecin.is_medecin())
        self.assertFalse(medecin.is_patient())

    def test_connexion_valide(self):
        logged = self.client.login(username='testpatient', password='test1234')
        self.assertTrue(logged)

    def test_connexion_invalide(self):
        logged = self.client.login(username='testpatient', password='mauvais')
        self.assertFalse(logged)