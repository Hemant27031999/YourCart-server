from rest_framework import serializers
from .models import *

class RegUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegUser
        fields = '__all__'

#class OrdersSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Orders
#        fields = ['order_id', 'product_id', 'phone_no']

class RegAddresses(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields='__all__'

class indep_AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model=indep_Addresses
        fields = '__all__'

class UserCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCache
        fields = '__all__'
