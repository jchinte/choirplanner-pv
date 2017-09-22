from django.shortcuts import render
from registration.views import RegistrationView
from .forms import PVRegistrationForm

# Create your views here.
class PVRegistrationView(RegistrationView):