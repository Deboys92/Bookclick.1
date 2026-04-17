#!/usr/bin/env python
# Fixed version for Railway deployment
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookclick.settings')
django.setup()

from accounts.models import User

def create_demo_users():
    """Crée des utilisateurs de démonstration pour la production"""
    
    demo_users = [
        {
            'email': 'admin@bookclick.com',
            'username': 'admin',
            'first_name': 'Admin',
            'last_name': 'BookClick',
            'password': 'admin123',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
        {
            'email': 'sandy@gmail.com',
            'username': 'sandy',
            'first_name': 'Sandy',
            'last_name': 'User',
            'password': 'sandy',
            'role': 'student',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'email': 'teacher@bookclick.com',
            'username': 'teacher',
            'first_name': 'Teacher',
            'last_name': 'Demo',
            'password': 'teacher123',
            'role': 'teacher',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'email': 'superadmin@bookclick.com',
            'username': 'superadmin',
            'first_name': 'Super',
            'last_name': 'Admin',
            'password': 'superadmin123',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    ]
    
    created_count = 0
    for user_data in demo_users:
        email = user_data.pop('email')
        password = user_data.pop('password')
        
        if not User.objects.filter(email=email).exists():
            if user_data.get('is_superuser', False):
                User.objects.create_superuser(email=email, password=password, **user_data)
            else:
                User.objects.create_user(email=email, password=password, **user_data)
            print(f"✅ Utilisateur créé : {email}")
            created_count += 1
        else:
            print(f"ℹ️  Utilisateur existe déjà : {email}")
    
    print(f"\n🎉 {created_count} utilisateurs créés avec succès!")
    print("\n📋 Comptes disponibles :")
    print("🔑 Admin: admin@bookclick.com / admin123")
    print("👨‍🎓 Étudiant: sandy@gmail.com / sandy")
    print("👨‍🏫 Professeur: teacher@bookclick.com / teacher123")
    print("⚡ SuperAdmin: superadmin@bookclick.com / superadmin123")

if __name__ == '__main__':
    create_demo_users()
