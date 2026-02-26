from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'phone_number', 'department', 'student_id',
            'profile_picture', 'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone_number',
            'department', 'student_id'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Password fields did not match.'
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request"""
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': 'Password fields did not match.'
            })
        return attrs
