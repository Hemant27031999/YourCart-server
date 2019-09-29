from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


#class SignUpForm(UserCreationForm):
#    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#    phone_no = forms.IntegerField(required=False, help_text='Optional.')
#    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
#    username = forms.CharField(max_length=255, )
#
#    class Meta:
#        model = User
#        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
#
#    def __str__(self):
#        return ("UserCreationForm")



class HotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ['name', 'hotel_Main_Img']

class AddressForm(forms.ModelForm):

    class Meta:
        model = Addresses
        fields = ['house_no', 'street', 'city', 'landmark', 'pincode', 'email']
