from rest_framework import serializers
from .models import RegUser, UserCache

class RegUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegUser
        fields = '__all__'

class UserCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCache
        fields = '__all__'