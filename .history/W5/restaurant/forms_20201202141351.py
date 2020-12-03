from django import forms
from django.db.models import fields
from .models import ElementAddress

class NearByReastaurants(forms.ModelForm):
    class Meta:
        model = ElementAddress
        fields = ('element',) 