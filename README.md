# MediBook — Intelligent Medical Appointment Management Platform

![Django](https://img.shields.io/badge/Django-4.x-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=flat-square&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square&logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange?style=flat-square&logo=githubactions)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-blueviolet?style=flat-square&logo=railway)

---

## Live Demo

**[https://medibook-production-ec9a.up.railway.app/](https://medibook-production-ec9a.up.railway.app/)**

---

## Description

**MediBook** is a web-based medical appointment management platform built with **Django**. It allows patients to search for doctors, check their availability, and book appointments. Doctors and administrators have dedicated dashboards to manage schedules, appointments, and consultation data.

The platform also integrates an **AI-powered feature** that helps patients find the right medical specialty based on their consultation reason.

---

## Features

### Visitor
- Browse the homepage and doctor listings
- Search doctors by name or specialty
- Register a patient account

### Patient
- Book, modify, or cancel appointments
- View doctor availability
- Track appointment history
- Receive notifications and reminders
- Use the AI assistant to find the right specialty

### Doctor
- Manage professional profile and specialties
- Set availability and time slots
- Confirm or cancel appointments
- View daily / weekly schedule
- Access personal statistics

### Administrator
- Manage user accounts, doctors, and specialties
- View all appointments and global statistics
- Control platform settings

---

## AI Feature — Specialty Orientation

The `ai_orientation` module analyzes the patient's consultation reason and suggests the most relevant medical specialty.

**Technical approach:**
- Text vectorization with **TF-IDF**
- Comparison using **cosine similarity**
- Implemented with **scikit-learn**

**Example:**
> Patient enters: *"chest pain, palpitations, shortness of breath"*
> Recommended specialty: **Cardiology**

> This feature provides indicative guidance only. It does not constitute a medical diagnosis.

---

## Data Models

### `CustomUser` — `accounts/models.py`
```python
class CustomUser(AbstractUser):
    role         = CharField(choices=['patient', 'medecin', 'admin'])
    telephone    = CharField()
    photo        = ImageField(upload_to='photos/')

    def is_patient() / is_medecin() / is_admin()
```

### `ProfilPatient` — `patients/models.py`
```python
class ProfilPatient(Model):
    user            = OneToOneField(CustomUser)
    date_naissance  = DateField()
    adresse         = TextField()
    groupe_sanguin  = CharField()
    allergies       = TextField()
```

### `Specialite` — `ai_orientation/models.py`
```python
class Specialite(Model):
    nom         = CharField()
    description = TextField()
    icone       = CharField()
```

### `Medecin` — `doctors/models.py`
```python
class Medecin(Model):
    user              = OneToOneField(CustomUser)
    specialite        = ForeignKey(Specialite)
    telephone         = CharField()
    adresse           = TextField()
    description       = TextField()
    annees_experience = IntegerField()
    photo             = ImageField()
    est_actif         = BooleanField()
```

### `Disponibilite` — `schedules/models.py`
```python
class Disponibilite(Model):
    medecin     = ForeignKey(Medecin)
    jour        = IntegerField(choices=[0..6])  # Monday to Sunday
    heure_debut = TimeField()
    heure_fin   = TimeField()
    duree_rdv   = IntegerField(default=30)      # in minutes
    est_actif   = BooleanField()
```

### `RendezVous` — `appointments/models.py`
```python
class RendezVous(Model):
    patient       = ForeignKey(CustomUser)
    medecin       = ForeignKey(Medecin)
    specialite    = ForeignKey(Specialite)
    date          = DateField()
    heure         = TimeField()
    motif         = TextField()
    statut        = CharField(choices=['en_attente', 'confirme', 'annule', 'termine', 'absent'])
    date_creation = DateTimeField(auto_now_add=True)
    notes_medecin = TextField()
```

### `Consultation` — `appointments/models.py`
```python
class Consultation(Model):
    rendez_vous   = OneToOneField(RendezVous)
    resume        = TextField()
    date_creation = DateTimeField(auto_now_add=True)
```

### `Notification` — `notifications/models.py`
```python
class Notification(Model):
    utilisateur   = ForeignKey(CustomUser)
    message       = TextField()
    lu            = BooleanField(default=False)
    date_creation = DateTimeField(auto_now_add=True)
```

### `Avis` — `doctors/models.py`
```python
class Avis(Model):
    patient       = ForeignKey(CustomUser)
    medecin       = ForeignKey(Medecin)
    note          = IntegerField(choices=[1..5])
    commentaire   = TextField()
    date_creation = DateTimeField(auto_now_add=True)

    # Constraint: one review per patient per doctor
    unique_together = ('patient', 'medecin')
```

---

## Project Structure

```
medibook/
├── accounts/           # User management & authentication
├── patients/           # Patient profiles
├── doctors/            # Doctors, specialties & reviews
├── appointments/       # Appointments & consultations
├── schedules/          # Doctor availability
├── dashboard/          # Patient, doctor & admin dashboards
├── ai_orientation/     # AI specialty recommendation module
├── notifications/      # Reminders & notifications
├── templates/          # HTML templates
├── static/             # CSS / JS assets
├── fixtures/           # Initial seed data
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
└── .github/workflows/  # CI/CD pipeline
```

---

## Tech Stack

| Layer            | Technology                        |
|------------------|-----------------------------------|
| Backend          | Django 4.x                        |
| Database         | PostgreSQL 15                     |
| Frontend         | Django Templates + Bootstrap      |
| AI               | Python, scikit-learn, TF-IDF      |
| Authentication   | Django Auth System                |
| WSGI Server      | Gunicorn                          |
| Reverse Proxy    | Nginx                             |
| Containerization | Docker + Docker Compose           |
| CI/CD            | GitHub Actions + Docker Hub       |
| Deployment       | Railway                           |

---

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the repository

```bash
git clone https://github.com/wll-hayat04/Medibook_app.git
cd Medibook_app
```

### 2. Configure environment variables

Create a `.env` file at the project root:

```env
DEBUG=False
SECRET_KEY=your_secret_key_here
DB_NAME=medibook_db
DB_USER=medibook_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:7009
```

> Never commit the `.env` file to GitHub.

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

App available at: **[http://localhost:7009](http://localhost:7009)**

Docker Compose automatically handles migrations, fixtures loading, and static files collection.

---

## Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

---

## CI/CD Pipeline (GitHub Actions)

On every push to `main`, the pipeline automatically:

1. Checks out the source code
2. Authenticates with Docker Hub
3. Builds the Docker image
4. Pushes the image to Docker Hub as `<username>/medibook:latest`

### Required GitHub Secrets

| Secret            | Description              |
|-------------------|--------------------------|
| `DOCKER_USERNAME` | Docker Hub username      |
| `DOCKER_PASSWORD` | Docker Hub access token  |

---

## Security

- Login required to book any appointment
- Strict data isolation — patients cannot view each other's appointments
- CSRF protection enabled on all forms
- Passwords hashed by Django's authentication system
- Sensitive variables stored in `.env`, never hardcoded
- `DEBUG=False` in production
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` properly configured

---

## License

This project is open source and available under the [MIT License](LICENSE).
