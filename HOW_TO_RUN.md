# 🚀 Comment Lancer le Projet BookClick

## 📍 Sur Cet Ordinateur (Actuel)

### Méthode 1 : Terminal Normal
```bash
# 1. Ouvrir un terminal
# 2. Naviguer vers le projet
cd "/home/deboys/Documents/last dance /final year project /Bookclick.1"

# 3. Activer l'environnement virtuel
source venv/bin/activate

# 4. Lancer le serveur
python manage.py runserver

# 5. Ouvrir le navigateur : http://localhost:8000
```

### Méthode 2 : VS Code
```bash
# 1. Ouvrir VS Code
# 2. File > Open Folder > Sélectionner "Bookclick.1"
# 3. Ouvrir le terminal intégré (Ctrl + ` ou View > Terminal)
# 4. Taper les commandes :

source venv/bin/activate
python manage.py runserver

# 5. Ctrl + Clic sur http://127.0.0.1:8000 dans le terminal
```

### Méthode 3 : PyCharm
```bash
# 1. Ouvrir PyCharm
# 2. Open Project > Sélectionner "Bookclick.1"
# 3. Configurer l'interpréteur Python :
#    - File > Settings > Project > Python Interpreter
#    - Sélectionner : venv/bin/python
# 4. Ouvrir le terminal en bas
# 5. Lancer : python manage.py runserver
```

---

## 💻 Sur un Autre Ordinateur

### Étape 1 : Copier le Projet

**Option A : USB/Disque Externe**
```bash
# Copier tout le dossier "Bookclick.1" sur une clé USB
# Coller sur le nouvel ordinateur
```

**Option B : Git (Recommandé)**
```bash
# Sur l'ordinateur actuel :
cd "/home/deboys/Documents/last dance /final year project /Bookclick.1"
git init
git add .
git commit -m "Initial commit"
# Puis push vers GitHub/GitLab

# Sur le nouvel ordinateur :
git clone <votre-repo-url>
cd Bookclick.1
```

**Option C : Compression**
```bash
# Créer une archive
cd "/home/deboys/Documents/last dance /final year project"
tar -czf bookclick.tar.gz "Bookclick.1"

# Ou avec zip
zip -r bookclick.zip "Bookclick.1"

# Transférer et extraire sur le nouvel ordinateur
```

### Étape 2 : Installation sur le Nouvel Ordinateur

#### Sur Linux/Mac
```bash
# 1. Installer Python (si pas déjà installé)
python3 --version  # Vérifier la version

# 2. Naviguer vers le projet
cd /chemin/vers/Bookclick.1

# 3. Créer un environnement virtuel
python3 -m venv venv

# 4. Activer l'environnement
source venv/bin/activate

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Appliquer les migrations
python manage.py migrate

# 7. Créer les données de test
python create_sample_data.py

# 8. Lancer le serveur
python manage.py runserver
```

#### Sur Windows
```bash
# 1. Installer Python depuis python.org (si pas déjà installé)

# 2. Ouvrir PowerShell ou CMD dans le dossier du projet
cd C:\chemin\vers\Bookclick.1

# 3. Créer un environnement virtuel
python -m venv venv

# 4. Activer l'environnement
venv\Scripts\activate

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Appliquer les migrations
python manage.py migrate

# 7. Créer les données de test
python create_sample_data.py

# 8. Lancer le serveur
python manage.py runserver
```

---

## 🌐 Accès depuis le Réseau

### Lancer pour Accès Réseau Local

```bash
# Permet l'accès depuis d'autres appareils (téléphone, tablette, autre PC)
python manage.py runserver 0.0.0.0:8000
```

### Trouver votre IP

**Linux/Mac :**
```bash
# Méthode 1
ifconfig | grep "inet "

# Méthode 2
hostname -I

# Méthode 3
ip addr show
```

**Windows :**
```bash
ipconfig
# Chercher "IPv4 Address"
```

### Accéder depuis un Autre Appareil

```
# Si votre IP est 192.168.1.100
http://192.168.1.100:8000

# Depuis votre téléphone/tablette sur le même WiFi
http://192.168.1.100:8000
```

### ⚠️ Important pour l'Accès Réseau

Modifier `bookclick/settings.py` :
```python
# Ajouter votre IP dans ALLOWED_HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.100', '*']
```

---

## 🔧 Ports Différents

```bash
# Port 8080
python manage.py runserver 8080

# Port 3000
python manage.py runserver 3000

# Port personnalisé avec accès réseau
python manage.py runserver 0.0.0.0:8080
```

---

## 🐳 Avec Docker (Avancé)

Si vous voulez utiliser Docker :

### Créer un Dockerfile
```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Lancer avec Docker
```bash
# Construire l'image
docker build -t bookclick .

# Lancer le conteneur
docker run -p 8000:8000 bookclick

# Accéder : http://localhost:8000
```

---

## 📱 Déploiement en Ligne

### Heroku (Gratuit)
```bash
# 1. Installer Heroku CLI
# 2. Se connecter
heroku login

# 3. Créer une app
heroku create bookclick-app

# 4. Ajouter PostgreSQL
heroku addons:create heroku-postgresql:mini

# 5. Déployer
git push heroku main

# 6. Migrer la base de données
heroku run python manage.py migrate

# 7. Créer un superuser
heroku run python manage.py createsuperuser
```

### PythonAnywhere (Gratuit)
```bash
# 1. Créer un compte sur pythonanywhere.com
# 2. Ouvrir un Bash console
# 3. Cloner le projet
git clone <votre-repo>

# 4. Créer un environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 bookclick

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Configurer Web app dans le dashboard
# 7. Pointer vers manage.py
```

---

## 🛠️ Commandes Utiles

### Arrêter le Serveur
```bash
# Dans le terminal où le serveur tourne
Ctrl + C
```

### Redémarrer le Serveur
```bash
# Arrêter (Ctrl + C) puis relancer
python manage.py runserver
```

### Désactiver l'Environnement Virtuel
```bash
deactivate
```

### Vérifier que Tout Fonctionne
```bash
# Vérifier les erreurs
python manage.py check

# Vérifier les migrations
python manage.py showmigrations

# Tester les imports
python manage.py shell
>>> from accounts.models import User
>>> User.objects.count()
```

---

## 🔍 Dépannage

### Erreur : "No module named 'django'"
```bash
# L'environnement virtuel n'est pas activé
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Erreur : "Port already in use"
```bash
# Le port 8000 est déjà utilisé
# Solution 1 : Utiliser un autre port
python manage.py runserver 8080

# Solution 2 : Tuer le processus sur le port 8000
# Linux/Mac :
lsof -ti:8000 | xargs kill -9
# Windows :
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erreur : "Database is locked"
```bash
# Fermer tous les shells Django ouverts
# Redémarrer le serveur
```

### Le CSS ne se charge pas
```bash
# Recollecte les fichiers statiques
python manage.py collectstatic --noinput --clear
```

---

## 📋 Checklist de Lancement

- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé
- [ ] Environnement virtuel activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` configuré
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Données de test créées (optionnel)
- [ ] Serveur lancé (`python manage.py runserver`)
- [ ] Navigateur ouvert sur http://localhost:8000

---

## 🎯 Raccourcis Rapides

### Script de Lancement Rapide (Linux/Mac)

Créer un fichier `start.sh` :
```bash
#!/bin/bash
source venv/bin/activate
python manage.py runserver
```

Rendre exécutable et lancer :
```bash
chmod +x start.sh
./start.sh
```

### Script de Lancement Rapide (Windows)

Créer un fichier `start.bat` :
```batch
@echo off
call venv\Scripts\activate
python manage.py runserver
pause
```

Double-cliquer sur `start.bat` pour lancer.

---

## 📞 Besoin d'Aide ?

- Consultez `COMPLETE_GUIDE.md` pour plus de détails
- Vérifiez `README.md` pour la documentation générale
- Lisez `API_DOCUMENTATION.md` pour l'API

---

## ✅ Résumé Ultra-Rapide

```bash
# LA COMMANDE MAGIQUE (tout-en-un)
cd "/home/deboys/Documents/last dance /final year project /Bookclick.1" && source venv/bin/activate && python manage.py runserver
```

Puis ouvrir : **http://localhost:8000** 🚀

---

**Bon développement ! 🎉**
