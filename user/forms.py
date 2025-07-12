from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import EmailField


from django.contrib.auth.models import User
from app_admin.models import FieldOffice

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data
       


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
        
class ProfileForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            self.fields['reports_to'].queryset = User.objects.all().exclude(id=user.id)
            self.fields['reports_to'].initial=User.objects.all().exclude(id=user.id).first()
            self.fields['field_office'].queryset=FieldOffice.objects.all()
        self.fields['first_name'].required = True 
        self.fields['last_name'].required = True
        self.fields['portfolio'].required = True
        self.fields['contact_number'].required = True
        self.fields['job_title'].required = True
     class Meta:
        model = Profile
        fields=['first_name',
            'last_name',
            'portfolio',
            'contact_number',
            'job_title',
            'portfolio',
            'reports_to',
            'field_office',
            'emp_id',
            ]

class ProfileFormAdd(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            self.fields['reports_to'].queryset = User.objects.all().exclude(id=user.id)
            self.fields['reports_to'].initial=User.objects.all().exclude(id=user.id).first()
            self.fields['field_office'].queryset=FieldOffice.objects.all()
        self.fields['first_name'].required = True 
        self.fields['last_name'].required = True
        self.fields['portfolio'].required = True
        self.fields['contact_number'].required = True
        self.fields['job_title'].required = True
     class Meta:
        model = Profile
        fields=['first_name',
            'last_name',
            'portfolio',
            'contact_number',
            'job_title',
            'portfolio',
            'reports_to',
            'field_office',
            'emp_id',
            ]
        
class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Ah, ah, ah. You didn't say the magic word!",
        "inactive": "Permission denied",
    }

class BasicUserDataForm(forms.Form):
  error_css_class = 'is-invalid'
  user_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})) 

  class Meta:
    model = User   


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            self.fields['reports_to'].queryset = User.objects.all().exclude(id=user.id)
            self.fields['reports_to'].initial=User.objects.all().exclude(id=user.id).first()
        self.fields['field_office'].queryset = FieldOffice.objects.all()
        
        self.fields['first_name'].required = True 
        self.fields['last_name'].required = True
        self.fields['field_office'].required = True
        self.fields['contact_number'].required = True
        self.fields['job_title'].required = True
    
    class Meta:
        model = Profile
        fields="__all__"
        exclude=['user']