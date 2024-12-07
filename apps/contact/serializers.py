from rest_framework import serializers
from .models import Contact
from django.core.validators import MinLengthValidator, MaxLengthValidator

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact_reason', 'message']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'message': {
                'required': True,
                'validators': [
                    MinLengthValidator(10),
                    MaxLengthValidator(1000)
                ]
            }
        }