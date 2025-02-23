from django.core.validators import validate_email
from django.db import IntegrityError
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from .utils import validate_phone, validate_email
from .models import UserProfile
from django.contrib.auth.models import User


class SignSerializer(serializers.Serializer):
    id = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    @staticmethod
    def validate_id(value):
        valid_email = validate_email(value.strip())
        valid_phone = validate_phone(value.strip().replace(' ', ''))

        if valid_email or valid_phone:
            return value
        raise ValidationError('Invalid email address or phone number')

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    @staticmethod
    def get_authenticated_user(validated_data):
        return authenticate(username=validated_data['id'], password=validated_data['password'])


class SignUpSerializer(SignSerializer):

    def create(self, validated_data):
        identifier = validated_data['id']
        password = validated_data['password']

        if validate_email(identifier):
            type_id = 'email'
        else:
            type_id = 'phone'

        try:
            user = User.objects.create_user(
                username=identifier,
                password=password,
            )
            UserProfile.objects.create(user=user, id_type=type_id)
        except IntegrityError:
            return False
        return user