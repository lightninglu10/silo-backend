"""
The custom form for signup to take last name and first name
"""

from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=300, label='first_name')
    last_name = forms.CharField(max_length=300, label='last_name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
