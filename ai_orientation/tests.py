from django.test import TestCase
from ai_orientation.views import SPECIALITES_DATA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def orienter(motif):
    specialites = list(SPECIALITES_DATA.keys())
    descriptions = list(SPECIALITES_DATA.values()) + [motif]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(descriptions)
    similarites = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
    return specialites[np.argmax(similarites)]

class TestAIOrientation(TestCase):

    def test_orientation_cardiologie(self):
        resultat = orienter('douleur poitrine palpitations essoufflement')
        self.assertEqual(resultat, 'Cardiologie')

    def test_orientation_dermatologie(self):
        resultat = orienter('boutons rougeurs demangeaisons peau acne')
        self.assertEqual(resultat, 'Dermatologie')

    def test_orientation_pediatrie(self):
        resultat = orienter('fievre enfant nourrisson bebe')
        self.assertEqual(resultat, 'Pédiatrie')

    def test_orientation_dentisterie(self):
        resultat = orienter('douleur dentaire carie gencive')
        self.assertEqual(resultat, 'Dentisterie')

    def test_specialites_disponibles(self):
        self.assertIn('Cardiologie', SPECIALITES_DATA)
        self.assertIn('Dermatologie', SPECIALITES_DATA)