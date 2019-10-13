from django.shortcuts import render
from .models import *
from base_tech.models import *

# Create your views here.
def check_vendor(request):
	if request.method == 'POST':
