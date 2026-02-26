# 🎓 BookClick - Guide Complet d'Utilisation

## 📋 Table des Matières

1. [Installation](#installation)
2. [Démarrage Rapide](#démarrage-rapide)
3. [Fonctionnalités](#fonctionnalités)
4. [Guide Utilisateur](#guide-utilisateur)
5. [Guide Administrateur](#guide-administrateur)
6. [Configuration Email](#configuration-email)
7. [API REST](#api-rest)
8. [Dépannage](#dépannage)

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip
- virtualenv (optionnel mais recommandé)

### Étapes d'Installation

```bash
# 1. Naviguer vers le projet
cd "/home/deboys/Documents/last dance /final year project /Bookclick.1"

# 2. Activer l'environnement virtuel
source venv/bin/activate

# 3. Installer les dépendances (déjà fait)
pip install -r requirements.txt

# 4. Appliquer les migrations (déjà fait)
python manage.py migrate

# 5. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 6. Lancer le serveur
python manage.py runserver
```

### Accès à l'Application

- **URL principale:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin
- **API REST:** http://localhost:8000/api/

---

## ⚡ Démarrage Rapide

### Comptes de Test Disponibles

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Admin** | admin@university.edu | admin123 |
| **Enseignant** | john.doe@university.edu | teacher123 |
| **Étudiant** | alice.johnson@university.edu | student123 |

### Première Connexion

1. Ouvrir http://localhost:8000
2. Cliquer sur "Login"
3. Utiliser un des comptes ci-dessus
4. Explorer le dashboard

---

## 🎯 Fonctionnalités

### ✅ Fonctionnalités Implémentées

#### Pour Tous les Utilisateurs
- ✅ Inscription et connexion
- ✅ Gestion du profil
- ✅ Consultation des salles disponibles
- ✅ Recherche et filtrage avancé
- ✅ Vérification de disponibilité
- ✅ Création de réservations
- ✅ Consultation de l'historique

#### Pour les Étudiants
- ✅ Réserver des salles
- ✅ Voir leurs réservations
- ✅ Annuler leurs réservations
- ✅ Recevoir des notifications

#### Pour les Enseignants
- ✅ Toutes les fonctionnalités étudiants
- ✅ Réserver pour des cours
- ✅ Gérer plusieurs réservations

#### Pour les Administrateurs
- ✅ Tableau de bord admin complet
- ✅ Gestion des utilisateurs
- ✅ Gestion des salles (CRUD)
- ✅ Approbation/rejet des réservations
- ✅ Statistiques d'utilisation
- ✅ Notifications par email

#### Système de Notifications
- ✅ Email de confirmation de réservation
- ✅ Email d'approbation
- ✅ Email de rejet
- ✅ Email d'annulation
- ✅ Rappels automatiques (24h avant)
- ✅ Notifications aux admins

---

## 👤 Guide Utilisateur

### 1. Inscription

1. Cliquer sur "Register" dans la barre de navigation
2. Remplir le formulaire :
   - Email institutionnel
   - Nom d'utilisateur
   - Mot de passe
   - Rôle (Student/Teacher)
   - Informations supplémentaires
3. Accepter les conditions
4. Cliquer sur "Register"

### 2. Connexion

1. Cliquer sur "Login"
2. Entrer email et mot de passe
3. Cocher "Remember me" (optionnel)
4. Cliquer sur "Login"

### 3. Consulter les Salles

1. Cliquer sur "Rooms" dans le menu
2. Utiliser les filtres :
   - Type de salle
   - Bâtiment
   - Capacité minimale
   - Équipements
3. Cliquer sur une salle pour voir les détails

### 4. Créer une Réservation

**Méthode 1 : Depuis la liste des salles**
1. Trouver la salle désirée
2. Cliquer sur "Book"
3. Remplir le formulaire
4. Soumettre

**Méthode 2 : Depuis le dashboard**
1. Cliquer sur "New Booking"
2. Sélectionner la salle
3. Remplir les détails
4. Soumettre

**Méthode 3 : Vérifier la disponibilité d'abord**
1. Cliquer sur "Check Availability"
2. Sélectionner salle, date, heure
3. Si disponible, cliquer sur "Book This Room Now"

### 5. Gérer ses Réservations

1. Aller dans "Bookings" ou "Dashboard"
2. Voir toutes les réservations
3. Actions disponibles :
   - **Voir** : Détails complets
   - **Modifier** : Si statut = PENDING
   - **Annuler** : Si statut = PENDING ou APPROVED

### 6. Statuts des Réservations

| Statut | Description | Actions |
|--------|-------------|---------|
| **PENDING** | En attente d'approbation | Modifier, Annuler |
| **APPROVED** | Approuvée | Annuler |
| **REJECTED** | Rejetée | Voir raison |
| **CANCELLED** | Annulée | Aucune |

---

## 👨‍💼 Guide Administrateur

### Accès au Dashboard Admin

1. Se connecter avec un compte admin
2. Cliquer sur "Admin" dans le menu
3. Ou accéder à http://localhost:8000/admin-dashboard/

### Tableau de Bord

Le dashboard admin affiche :
- **Statistiques** : Utilisateurs, salles, réservations
- **Réservations en attente** : À approuver/rejeter
- **Réservations récentes** : Historique
- **Statistiques des salles** : Les plus réservées

### Gérer les Réservations

#### Approuver une Réservation
1. Aller dans "Pending Bookings"
2. Cliquer sur "Approve"
3. Confirmer
4. L'utilisateur reçoit un email

#### Rejeter une Réservation
1. Cliquer sur "Reject"
2. Entrer la raison du rejet
3. Confirmer
4. L'utilisateur reçoit un email avec la raison

### Gérer les Salles

#### Ajouter une Salle
1. Cliquer sur "Add New Room"
2. Remplir le formulaire :
   - Nom de la salle
   - Type
   - Bâtiment
   - Étage
   - Capacité
   - Description
   - Statut
   - Équipements (cocher les cases)
   - Image (optionnel)
3. Cliquer sur "Create Room"

#### Modifier une Salle
1. Aller dans "Rooms"
2. Cliquer sur une salle
3. Cliquer sur "Edit Room"
4. Modifier les informations
5. Sauvegarder

#### Supprimer une Salle
1. Voir les détails de la salle
2. Cliquer sur "Delete Room"
3. Confirmer la suppression

### Gérer les Utilisateurs

1. Accéder à http://localhost:8000/admin/
2. Cliquer sur "Users"
3. Actions disponibles :
   - Voir/modifier utilisateurs
   - Changer les rôles
   - Activer/désactiver comptes
   - Vérifier les emails

---

## 📧 Configuration Email

### Configuration de Base

Éditer le fichier `.env` :

```bash
# Pour Gmail (recommandé pour les tests)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@university.edu
```

### Configuration Gmail

1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application :
   - https://myaccount.google.com/apppasswords
3. Utiliser ce mot de passe dans `.env`

### Test des Emails

```bash
# Mode console (pour développement)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Les emails s'afficheront dans la console au lieu d'être envoyés.

### Rappels Automatiques

Pour envoyer des rappels 24h avant les réservations :

```bash
python manage.py send_booking_reminders
```

**Automatiser avec cron (Linux/Mac) :**

```bash
crontab -e
# Ajouter :
0 9 * * * cd /path/to/bookclick && /path/to/venv/bin/python manage.py send_booking_reminders
```

Voir `EMAIL_SETUP.md` pour plus de détails.

---

## 🔌 API REST

### Authentification

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@university.edu","password":"admin123"}'

# Réponse :
{
  "user": {...},
  "token": "votre-token-ici",
  "message": "Login successful"
}
```

### Utiliser le Token

```bash
# Ajouter le header Authorization
curl -X GET http://localhost:8000/api/rooms/ \
  -H "Authorization: Token votre-token-ici"
```

### Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register/` | Inscription |
| POST | `/api/auth/login/` | Connexion |
| POST | `/api/auth/logout/` | Déconnexion |
| GET | `/api/auth/profile/` | Profil utilisateur |
| GET | `/api/rooms/` | Liste des salles |
| POST | `/api/rooms/` | Créer salle (admin) |
| GET | `/api/rooms/{id}/` | Détails salle |
| GET | `/api/bookings/` | Liste réservations |
| POST | `/api/bookings/` | Créer réservation |
| GET | `/api/bookings/{id}/` | Détails réservation |
| POST | `/api/bookings/{id}/approve/` | Approuver (admin) |
| POST | `/api/bookings/{id}/reject/` | Rejeter (admin) |
| POST | `/api/bookings/{id}/cancel/` | Annuler |
| GET | `/api/bookings/check_availability/` | Vérifier disponibilité |

Voir `API_DOCUMENTATION.md` pour la documentation complète.

---

## 🔧 Dépannage

### Le serveur ne démarre pas

```bash
# Vérifier les erreurs
python manage.py check

# Vérifier les migrations
python manage.py showmigrations

# Réappliquer les migrations
python manage.py migrate
```

### Erreur "No module named..."

```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Les fichiers statiques ne se chargent pas

```bash
# Recollecte les fichiers statiques
python manage.py collectstatic --noinput --clear
```

### Problème de base de données

```bash
# Supprimer et recréer la base
rm db.sqlite3
python manage.py migrate
python create_sample_data.py
```

### Les emails ne s'envoient pas

1. Vérifier la configuration dans `.env`
2. Utiliser le mode console pour tester :
   ```bash
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```
3. Voir `EMAIL_SETUP.md` pour plus d'aide

### Erreur 404 sur les pages

Vérifier que toutes les URLs sont correctement configurées :
```bash
python manage.py show_urls  # Si django-extensions installé
```

---

## 📊 Commandes Utiles

```bash
# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Lancer sur un port différent
python manage.py runserver 8080

# Lancer en mode accessible depuis le réseau
python manage.py runserver 0.0.0.0:8000

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Shell Django
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic

# Envoyer les rappels
python manage.py send_booking_reminders

# Tests
python manage.py test
```

---

## 📁 Structure du Projet

```
Bookclick.1/
├── accounts/              # Gestion utilisateurs
│   ├── models.py         # Modèle User
│   ├── views.py          # API views
│   ├── views_frontend.py # Frontend views
│   ├── serializers.py    # DRF serializers
│   └── urls.py           # URLs
├── rooms/                # Gestion salles
│   ├── models.py         # Modèle Room
│   ├── views.py          # API views
│   ├── views_frontend.py # Frontend views
│   └── ...
├── bookings/             # Réservations
│   ├── models.py         # Modèle Booking
│   ├── views.py          # API views
│   ├── views_frontend.py # Frontend views
│   ├── emails.py         # Système email
│   └── management/       # Commands
├── templates/            # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── accounts/
│   ├── rooms/
│   └── bookings/
├── static_dev/           # Fichiers statiques
│   ├── css/
│   └── js/
├── media/                # Uploads
├── manage.py             # Django CLI
├── requirements.txt      # Dépendances
├── .env                  # Configuration
└── db.sqlite3           # Base de données
```

---

## 🎓 Conseils d'Utilisation

### Pour les Étudiants
- Réservez à l'avance
- Vérifiez la disponibilité avant de réserver
- Annulez si vous ne pouvez pas venir
- Respectez les horaires

### Pour les Enseignants
- Planifiez vos cours à l'avance
- Vérifiez les équipements disponibles
- Informez les étudiants de la salle

### Pour les Admins
- Approuvez rapidement les réservations
- Maintenez les informations des salles à jour
- Surveillez les statistiques d'utilisation
- Gérez les conflits de réservation

---

## 📞 Support

- **Documentation:** Voir les fichiers .md dans le projet
- **Email:** support@university.edu
- **Issues:** Créer un ticket sur le système de gestion

---

## 🎉 Félicitations !

Vous êtes maintenant prêt à utiliser BookClick !

Pour toute question, consultez les autres fichiers de documentation :
- `README.md` - Vue d'ensemble
- `API_DOCUMENTATION.md` - Documentation API
- `EMAIL_SETUP.md` - Configuration email
- `PROJECT_STATUS.md` - État du projet
- `QUICKSTART.md` - Démarrage rapide
