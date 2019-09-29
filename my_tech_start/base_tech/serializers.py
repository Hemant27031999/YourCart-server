from rest_framework import serializers
from .models import RegUser

class RegUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegUser
        fields = '__all__'