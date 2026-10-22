from django import forms
from .models import candidate

class Candidateform(forms.ModelForm):


    class Meta:
        model = candidate

        fields = ['name','email','age']


        widgets = {
            'name':forms.TextInput(attrs={'placeholder': 'Enter full name '}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter your email'}),
            'age':forms.NumberInput(attrs={'placeholder':'Enter your age'})
        }