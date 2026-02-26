# BookClick - Classroom Management & Booking Platform

A comprehensive web application for managing and booking classroom spaces on university campuses.

## Features

### User Roles
- **Students**: Browse and book available rooms
- **Teachers**: Reserve rooms for courses and activities
- **Administrators**: Manage accounts, validate/cancel bookings, add rooms, view statistics

### Core Functionality
- ✅ Authentication with institutional email
- ✅ Room management (CRUD operations)
- ✅ Real-time booking system with availability checking
- ✅ Calendar view (day/week/month)
- ✅ Admin dashboard with statistics
- ✅ Email notifications
- ✅ Advanced search and filtering
- ✅ Responsive design (mobile, tablet, desktop)

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: PostgreSQL (SQLite for development)
- **Task Queue**: Celery + Redis
- **Email**: SMTP

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite works for development)
- Redis (for async tasks)

### Setup Instructions

1. **Clone the repository**
```bash
cd "/home/deboys/Documents/last dance /final year project /Bookclick.1"
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load initial data (optional)**
```bash
python manage.py loaddata initial_data.json
```

8. **Run development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Main app: http://localhost:8000
- Admin panel: http://localhost:8000/admin
- API: http://localhost:8000/api/

## Database Configuration

### For Development (SQLite)
In `.env`:
```
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### For Production (PostgreSQL)
In `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bookclick_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

Create PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE bookclick_db;
CREATE USER bookclick_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE bookclick_db TO bookclick_user;
\q
```

## Project Structure

```
bookclick/
├── manage.py
├── bookclick/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User management
├── rooms/                  # Room management
├── bookings/               # Booking system
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
└── media/                  # User uploads
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/password-reset/` - Password reset

### Rooms
- `GET /api/rooms/` - List all rooms
- `POST /api/rooms/` - Create room (admin only)
- `GET /api/rooms/{id}/` - Room details
- `PUT /api/rooms/{id}/` - Update room (admin only)
- `DELETE /api/rooms/{id}/` - Delete room (admin only)

### Bookings
- `GET /api/bookings/` - List bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/{id}/` - Booking details
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking

### Dashboard
- `GET /api/dashboard/stats/` - Admin statistics
- `GET /api/dashboard/pending/` - Pending bookings

## Running Tests

```bash
python manage.py test
```

## Deployment

For production deployment, see `DEPLOYMENT.md`

## License

MIT License

## Support

For issues and questions, contact: support@university.edu
