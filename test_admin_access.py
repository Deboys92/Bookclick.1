#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookclick.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

def test_admin_access():
    print("🔍 TEST D'ACCÈS ADMIN DJANGO")
    print("=" * 50)
    
    # Test 1: Vérifier les utilisateurs
    print("\n1️⃣ Utilisateurs dans la base :")
    for user in User.objects.all():
        print(f"   📧 {user.email}")
        print(f"   🔐 Staff: {user.is_staff} | Superuser: {user.is_superuser}")
        print(f"   ✅ Actif: {user.is_active}")
        print()
    
    # Test 2: Tester l'authentification
    print("2️⃣ Test d'authentification :")
    test_users = [
        ('admin@bookclick.com', 'admin123'),
        ('sandy@gmail.com', 'sandy'),
        ('superadmin@bookclick.com', 'superadmin123')
    ]
    
    for email, password in test_users:
        user = authenticate(username=email, password=password)
        if user:
            print(f"   ✅ {email}: Authentifié | Staff: {user.is_staff} | Superuser: {user.is_superuser}")
        else:
            print(f"   ❌ {email}: Échec authentification")
    
    # Test 3: Vérifier si l'admin Django est accessible
    print("\n3️⃣ Configuration admin Django :")
    try:
        from django.contrib import admin
        print("   ✅ Admin Django importé avec succès")
        print(f"   📋 Nombre de modèles enregistrés: {len(admin.site._registry)}")
    except Exception as e:
        print(f"   ❌ Erreur admin Django: {e}")

if __name__ == '__main__':
    test_admin_access()
