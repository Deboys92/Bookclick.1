from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Custom User model with role-based access
    Roles: STUDENT, TEACHER, ADMIN
    """
    
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('ADMIN', 'Administrator'),
    )
    
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text='Institutional email address'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Department or Faculty'
    )
    student_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text='Student or Employee ID'
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    is_verified = models.BooleanField(
        default=False,
        help_text='Email verification status'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def is_student(self):
        return self.role == 'STUDENT'
    
    def is_teacher(self):
        return self.role == 'TEACHER'
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def full_name(self):
        return self.get_full_name() or self.username
