# home/forms.py
from django import forms
from .models import User, NGO

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password', 'phone1', 'phone2', 'house_no', 'city', 'pin', 'state']

class NGOForm(forms.ModelForm):
    class Meta:
        model = NGO
        fields = ['ngo_id', 'ngo_name', 'ngo_email', 'phone1', 'phone2', 'building_house_no', 'city', 'pin', 'state']



