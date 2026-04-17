#!/usr/bin/env python
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
        },
        {
            'email': 'sandy@gmail.com',
            'username': 'sandy',
            'first_name': 'Sandy',
            'last_name': 'User',
            'password': 'sandy',
            'role': 'student',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'email': 'teacher@bookclick.com',
            'username': 'teacher',
            'first_name': 'Teacher',
            'last_name': 'Demo',
            'password': 'teacher123',
            'role': 'teacher',
            'is_staff': False,
            'is_superuser': False,
        },
    ]
    
    created_count = 0
    for user_data in demo_users:
        email = user_data.pop('email')
        password = user_data.pop('password')
        
        if not User.objects.filter(email=email).exists():
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

if __name__ == '__main__':
    create_demo_users()
