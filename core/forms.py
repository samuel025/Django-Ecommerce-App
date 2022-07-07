from django import forms
from allauth.account.forms import SignupForm


class CheckoutForm(forms.Form):
	street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'1234 main str',
			'class': 'form-c'
		}))
	apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Apartment or Suite',
			'class': 'form-c'
		}))
	phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Phone Number',
			'class': 'form-c'
		}))
		

class CustomSignUpForm(SignupForm):
	first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={
			'placeholder':'First Name',
		}))
	last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={
			'placeholder':'Last Name',
		}))

	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()
		return user