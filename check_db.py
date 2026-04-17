#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookclick.settings')
django.setup()

from django.db import connection
from accounts.models import User
from rooms.models import Room
from bookings.models import Booking

print("=" * 50)
print("ÉTAT DE LA BASE DE DONNÉES")
print("=" * 50)

print(f"Base de données : {connection.vendor}")
print(f"Nom de la base : {connection.settings_dict['NAME']}")
print(f"Hôte : {connection.settings_dict.get('HOST', 'N/A')}")
print(f"Port : {connection.settings_dict.get('PORT', 'N/A')}")
print()

print("STATISTIQUES DES DONNÉES :")
print(f"  Utilisateurs : {User.objects.count()}")
print(f"  Salles : {Room.objects.count()}")
print(f"  Réservations : {Booking.objects.count()}")

if User.objects.exists():
    print()
    print("PREMIER UTILISATEUR :")
    user = User.objects.first()
    print(f"  Email : {user.email}")
    print(f"  Rôle : {user.role}")
    print(f"  Créé le : {user.created_at}")

if Room.objects.exists():
    print()
    print("PREMIÈRE SALLE :")
    room = Room.objects.first()
    print(f"  Nom : {room.name}")
    print(f"  Type : {room.room_type}")
    print(f"  Capacité : {room.capacity}")

print("=" * 50)
