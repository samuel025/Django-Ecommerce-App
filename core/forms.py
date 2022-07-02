from django import forms
from allauth.account.forms import SignupForm


class CheckoutForm(forms.Form):
	street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'1234 main str',
			'class': 'form-control'
		}))
	apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Apartment or Suite',
			'class': 'form-control'
		}))
	phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Phone Number',
			'class': 'form-control'
		}))
	set_default_shipping = forms.BooleanField(required=False)
	use_default_shipping = forms.BooleanField(required=False)
	
	

class CustomSignUpForm(SignupForm):
	first_name = forms.CharField(max_length=30, label='First Name')
	last_name = forms.CharField(max_length=30, label='Last Name')

	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()
		return user