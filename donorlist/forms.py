from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		# Assign profile model to model
		model = Profile
		# Defines fields of the form to update profile information
		fields = ['first_name', 'last_name', 'birth_date', 'city', 'email_address', 'blood_type']

class EmailSendForm(forms.Form):
	# TODO: set max size...
	mail_body = forms.CharField(label="", widget=forms.Textarea())