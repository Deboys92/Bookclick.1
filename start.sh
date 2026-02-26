#!/bin/bash

# BookClick - Script de Lancement Rapide
# Usage: ./start.sh

echo "🚀 Démarrage de BookClick..."
echo ""

# Activer l'environnement virtuel
echo "📦 Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier que Django est installé
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django n'est pas installé!"
    echo "📥 Installation des dépendances..."
    pip install -r requirements.txt
fi

# Appliquer les migrations si nécessaire
echo "🔄 Vérification des migrations..."
python manage.py migrate --check 2>/dev/null || python manage.py migrate

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput --clear > /dev/null 2>&1

echo ""
echo "✅ BookClick est prêt!"
echo ""
echo "🌐 Accès:"
echo "   - Local:   http://localhost:8000"
echo "   - Admin:   http://localhost:8000/admin"
echo "   - API:     http://localhost:8000/api"
echo ""
echo "🔑 Comptes de test:"
echo "   - Admin:   admin@university.edu / admin123"
echo "   - Teacher: john.doe@university.edu / teacher123"
echo "   - Student: alice.johnson@university.edu / student123"
echo ""
echo "⏹️  Pour arrêter: Ctrl + C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Lancer le serveur
python manage.py runserver
