from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.contrib.auth.decorators import login_required

SPECIALITES_DATA = {
    "Cardiologie": "douleur poitrine coeur palpitations essoufflement tension arterielle cardiaque infarctus tachycardie",
    "Dermatologie": "peau boutons rougeurs acne eczema psoriasis demangeaisons eruption tache grain beaute",
    "Pédiatrie": "enfant bebe fievre nourrisson croissance vaccination pediatrique",
    "Médecine générale": "fatigue fievre toux rhume grippe mal tete general consultation",
    "Gynécologie": "femme grossesse menstruation cycle uterus ovaire contraception gyneco",
    "Ophtalmologie": "oeil vision lunettes myopie cataracte glaucome vue trouble",
    "Dentisterie": "dent dentaire carie douleur dentaire gencive extraction orthodontie",
    "ORL": "oreille nez gorge sinusite angine otite audition rhinite",
    "Neurologie": "tete migraine epilepsie vertige paralysie neurologique cerveau",
    "Radiologie": "radio scanner irm imagerie radiographie echographie",
}

@login_required

def ai_orientation(request):
    resultat = None
    suggestions = []
    motif = ""

    if request.method == 'POST':
        motif = request.POST.get('motif', '').strip()
        if motif:
            specialites = list(SPECIALITES_DATA.keys())
            descriptions = list(SPECIALITES_DATA.values())
            descriptions_avec_motif = descriptions + [motif]

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(descriptions_avec_motif)
            similarites = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

            indices_tries = np.argsort(similarites)[::-1]
            resultat = specialites[indices_tries[0]]
            suggestions = [specialites[i] for i in indices_tries[1:3] if similarites[i] > 0]

    return render(request, 'ai_orientation/orientation.html', {
        'resultat': resultat,
        'suggestions': suggestions,
        'motif': motif,
    })



def chatbot(request):
    reponse = None
    question = ""

    FAQ = {
        # Rendez-vous
        "prendre rendez-vous": "Pour prendre un rendez-vous, connectez-vous à votre compte patient, allez dans 'Médecins', choisissez un médecin et cliquez sur 'Prendre rendez-vous'.",
        "annuler rendez-vous": "Pour annuler un rendez-vous, allez dans 'Mes RDV', cliquez sur l'icône ❌ à côté du rendez-vous concerné.",
        "modifier rendez-vous": "Pour modifier un rendez-vous, allez dans 'Mes RDV', cliquez sur l'icône ✏️ à côté du rendez-vous concerné.",
        "voir mes rendez-vous": "Vos rendez-vous sont disponibles dans la section 'Mes RDV' accessible depuis le menu en haut.",
        "rendez-vous confirmé": "Un rendez-vous est confirmé lorsque le médecin l'a accepté. Vous recevrez une notification.",
        "créneau disponible": "Les créneaux disponibles s'affichent automatiquement après avoir choisi une date lors de la prise de rendez-vous.",

        # Compte
        "créer compte": "Pour créer un compte, cliquez sur 'S'inscrire' en haut à droite et remplissez le formulaire patient.",
        "mot de passe oublié": "Cliquez sur 'Mot de passe oublié ?' sur la page de connexion. Un lien vous sera envoyé par email.",
        "modifier profil": "Pour modifier votre profil, connectez-vous et allez dans 'Mon profil' depuis le menu.",
        "changer photo": "Dans 'Mon profil', cliquez sur la zone de photo pour uploader une nouvelle image.",
        "se connecter": "Cliquez sur 'Connexion' en haut à droite, choisissez votre rôle (Patient ou Médecin) et entrez vos identifiants.",

        # Médecins
        "trouver médecin": "Allez dans 'Médecins' depuis le menu. Vous pouvez filtrer par spécialité ou rechercher par nom.",
        "spécialité": "Utilisez notre module d'orientation IA pour trouver la spécialité adaptée à vos symptômes.",
        "disponibilité médecin": "Les disponibilités d'un médecin s'affichent sur sa page de profil.",
        "avis médecin": "Après une consultation, vous pouvez laisser un avis et une note au médecin depuis son profil.",

        # IA
        "orientation ia": "Notre module IA analyse vos symptômes et vous oriente vers la spécialité médicale appropriée. Accédez-y via 'Orientation IA' dans le menu.",
        "symptômes": "Décrivez vos symptômes dans le module 'Orientation IA' et notre algorithme vous recommandera une spécialité.",

        # Général
        "horaires": "Les horaires de chaque médecin sont définis individuellement. Consultez le profil du médecin pour voir ses disponibilités.",
        "contact": "Contactez-nous via la page 'Contact' ou par email à contact@medibook.ma.",
        "urgence": "En cas d'urgence médicale, appelez le 15 (SAMU) ou le 150. MediBook n'est pas un service d'urgence.",
        "notification": "Vous recevez une notification automatique lors de chaque réservation ou modification de rendez-vous.",
        "imprimer rdv": "Dans 'Mes RDV', cliquez sur l'icône 👁️ pour voir le détail du RDV, puis cliquez sur 'Imprimer'.",
        "calendrier": "Vos rendez-vous sont visibles dans une vue calendrier. Cliquez sur 'Vue calendrier' dans 'Mes RDV'.",
    }

    if request.method == 'POST':
        question = request.POST.get('question', '').strip().lower()

        if question:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np

            questions_faq = list(FAQ.keys())
            reponses_faq = list(FAQ.values())

            corpus = questions_faq + [question]
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(corpus)
            similarites = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

            meilleur_index = np.argmax(similarites)
            meilleur_score = similarites[meilleur_index]

            if meilleur_score > 0.1:
                reponse = reponses_faq[meilleur_index]
            else:
                reponse = "Je n'ai pas trouvé de réponse à votre question. Veuillez contacter notre équipe via la page Contact ou appeler le +212 5XX-XXXXXX."

    return render(request, 'ai_orientation/chatbot.html', {
        'reponse': reponse,
        'question': question,
    })