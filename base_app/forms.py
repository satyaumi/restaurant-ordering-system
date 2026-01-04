from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import PasswordResetForm

class CustomLoginForm(AuthenticationForm):
    username =forms.CharField(
        widget =forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'
    }))

    password =forms.CharField(
        widget =forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class CustomSignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }),
        label=''
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        label=''
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label=''
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        label=''
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class UsernameEmailPasswordResetForm(PasswordResetForm):
    username =forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Username'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not User.objects.filter(username=username, email=email).exists():
            raise forms.ValidationError(
                "Username and email do not match."
            )

        return cleaned_data
