#!/usr/bin/env python
"""
Script to create sample data for BookClick application
Run: python manage.py shell < create_sample_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookclick.settings')
django.setup()

from accounts.models import User
from rooms.models import Room
from bookings.models import Booking
from datetime import date, time, timedelta

print("Creating sample data...")

# Create users
print("\n1. Creating users...")

# Admin user
admin, created = User.objects.get_or_create(
    email='admin@university.edu',
    defaults={
        'username': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'ADMIN',
        'is_staff': True,
        'is_superuser': True,
        'is_verified': True,
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"  ✓ Admin created: {admin.email}")
else:
    print(f"  - Admin already exists: {admin.email}")

# Teacher users
teacher1, created = User.objects.get_or_create(
    email='john.doe@university.edu',
    defaults={
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'role': 'TEACHER',
        'department': 'Computer Science',
        'student_id': 'T001',
        'is_verified': True,
    }
)
if created:
    teacher1.set_password('teacher123')
    teacher1.save()
    print(f"  ✓ Teacher created: {teacher1.email}")

teacher2, created = User.objects.get_or_create(
    email='jane.smith@university.edu',
    defaults={
        'username': 'janesmith',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'role': 'TEACHER',
        'department': 'Mathematics',
        'student_id': 'T002',
        'is_verified': True,
    }
)
if created:
    teacher2.set_password('teacher123')
    teacher2.save()
    print(f"  ✓ Teacher created: {teacher2.email}")

# Student users
student1, created = User.objects.get_or_create(
    email='alice.johnson@university.edu',
    defaults={
        'username': 'alicejohnson',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'role': 'STUDENT',
        'department': 'Computer Science',
        'student_id': 'S001',
        'is_verified': True,
    }
)
if created:
    student1.set_password('student123')
    student1.save()
    print(f"  ✓ Student created: {student1.email}")

student2, created = User.objects.get_or_create(
    email='bob.williams@university.edu',
    defaults={
        'username': 'bobwilliams',
        'first_name': 'Bob',
        'last_name': 'Williams',
        'role': 'STUDENT',
        'department': 'Engineering',
        'student_id': 'S002',
        'is_verified': True,
    }
)
if created:
    student2.set_password('student123')
    student2.save()
    print(f"  ✓ Student created: {student2.email}")

# Create rooms
print("\n2. Creating rooms...")

rooms_data = [
    {
        'name': 'Room 101',
        'room_type': 'CLASSROOM',
        'building': 'Main Building',
        'floor': '1st Floor',
        'capacity': 30,
        'description': 'Standard classroom with modern facilities',
        'has_projector': True,
        'has_whiteboard': True,
        'has_wifi': True,
    },
    {
        'name': 'Lab A',
        'room_type': 'LABORATORY',
        'building': 'Science Building',
        'floor': '2nd Floor',
        'capacity': 25,
        'description': 'Computer laboratory with 25 workstations',
        'has_projector': True,
        'has_computer': True,
        'has_wifi': True,
        'has_ac': True,
    },
    {
        'name': 'Auditorium',
        'room_type': 'AUDITORIUM',
        'building': 'Main Building',
        'floor': 'Ground Floor',
        'capacity': 200,
        'description': 'Large auditorium for conferences and events',
        'has_projector': True,
        'has_audio_system': True,
        'has_wifi': True,
        'has_ac': True,
    },
    {
        'name': 'Meeting Room 1',
        'room_type': 'MEETING_ROOM',
        'building': 'Administration Building',
        'floor': '3rd Floor',
        'capacity': 15,
        'description': 'Small meeting room for group discussions',
        'has_whiteboard': True,
        'has_wifi': True,
    },
    {
        'name': 'Room 205',
        'room_type': 'CLASSROOM',
        'building': 'Main Building',
        'floor': '2nd Floor',
        'capacity': 40,
        'description': 'Large classroom',
        'has_projector': True,
        'has_whiteboard': True,
        'has_wifi': True,
        'has_ac': True,
    },
]

for room_data in rooms_data:
    room, created = Room.objects.get_or_create(
        name=room_data['name'],
        defaults=room_data
    )
    if created:
        print(f"  ✓ Room created: {room.name}")
    else:
        print(f"  - Room already exists: {room.name}")

# Create sample bookings
print("\n3. Creating sample bookings...")

today = date.today()
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(days=7)

bookings_data = [
    {
        'user': teacher1,
        'room': Room.objects.get(name='Room 101'),
        'title': 'Introduction to Python',
        'description': 'First lecture on Python programming',
        'date': tomorrow,
        'start_time': time(9, 0),
        'end_time': time(11, 0),
        'number_of_attendees': 25,
        'status': 'APPROVED',
    },
    {
        'user': teacher2,
        'room': Room.objects.get(name='Room 205'),
        'title': 'Calculus Class',
        'description': 'Advanced calculus lecture',
        'date': tomorrow,
        'start_time': time(14, 0),
        'end_time': time(16, 0),
        'number_of_attendees': 30,
        'status': 'APPROVED',
    },
    {
        'user': student1,
        'room': Room.objects.get(name='Meeting Room 1'),
        'title': 'Study Group',
        'description': 'Group study session for final exams',
        'date': next_week,
        'start_time': time(10, 0),
        'end_time': time(12, 0),
        'number_of_attendees': 10,
        'status': 'PENDING',
    },
    {
        'user': teacher1,
        'room': Room.objects.get(name='Lab A'),
        'title': 'Programming Lab',
        'description': 'Hands-on programming session',
        'date': next_week,
        'start_time': time(13, 0),
        'end_time': time(15, 0),
        'number_of_attendees': 20,
        'status': 'PENDING',
    },
]

for booking_data in bookings_data:
    # Check if booking already exists
    existing = Booking.objects.filter(
        room=booking_data['room'],
        date=booking_data['date'],
        start_time=booking_data['start_time']
    ).first()
    
    if not existing:
        booking = Booking.objects.create(**booking_data)
        print(f"  ✓ Booking created: {booking.title} - {booking.date}")
    else:
        print(f"  - Booking already exists: {booking_data['title']}")

print("\n✅ Sample data created successfully!")
print("\n📝 Login credentials:")
print("  Admin: admin@university.edu / admin123")
print("  Teacher: john.doe@university.edu / teacher123")
print("  Student: alice.johnson@university.edu / student123")
