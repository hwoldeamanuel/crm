from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("email","username")
       


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields ="__all__"
        
class ProfileForm(forms.ModelForm):
     
     class Meta:
        model = User
        fields ="__all__"