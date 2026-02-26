# BookClick - Quick Start Guide

## Installation Rapide

```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Lancer le serveur
python manage.py runserver

# 3. Accéder à l'application
# Ouvrir: http://localhost:8000
```

## Comptes de Test

**Admin:**
- Email: admin@university.edu
- Password: admin123

**Enseignant:**
- Email: john.doe@university.edu  
- Password: teacher123

**Étudiant:**
- Email: alice.johnson@university.edu
- Password: student123

## URLs Principales

- **Home:** http://localhost:8000/
- **Login:** http://localhost:8000/login/
- **Dashboard:** http://localhost:8000/dashboard/
- **Rooms:** http://localhost:8000/rooms/
- **Bookings:** http://localhost:8000/bookings/
- **Admin Panel:** http://localhost:8000/admin/
- **API Docs:** http://localhost:8000/api/

## Fonctionnalités

✅ Authentification complète
✅ Gestion des salles (CRUD)
✅ Système de réservation
✅ Vérification de disponibilité
✅ Approbation admin
✅ Filtres et recherche
✅ API REST complète
✅ Interface responsive

## Structure

```
bookclick/
├── accounts/      # Gestion utilisateurs
├── rooms/         # Gestion salles
├── bookings/      # Réservations
├── templates/     # Templates HTML
├── static_dev/    # CSS/JS
└── media/         # Uploads
```

## Commandes Utiles

```bash
# Créer superuser
python manage.py createsuperuser

# Migrations
python manage.py makemigrations
python manage.py migrate

# Collecter static files
python manage.py collectstatic

# Tests
python manage.py test
```

## Support

Pour questions: support@university.edu
