from django.core.validators import validate_email
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .utils import validate_phone, validate_email
from .models import User

class SignUpSerializer(serializers.Serializer):
    id = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)
    token = serializers.CharField(read_only=True)

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


    def create(self, validated_data):
        identifier = validated_data['id']
        password = validated_data['password']

        if validate_email(identifier):
            type_id = '1'
        else:
            type_id = '2'

        user, _ = User.objects.get_or_create(
            username=identifier,
            password=password,
            type_id=type_id
        )

        return user