from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User,Location, Patient


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'})
    )  # <-- Missing closing parenthesis added here
    nin = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your NIN'})
    )
    marital_status = forms.ChoiceField(
        choices=[('Single', 'Single'), ('Married', 'Married')],
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth', 'nin', 'marital_status']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['village', 'parish', 'sub_county', 'district', 'address']
        widgets = {
            'village': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your village'}),
            'parish': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your parish'}),
            'sub_county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your sub-county'}),
            'district': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your district'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter your address'}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'home_address', 'number_of_children', 'date_of_last_period', 'occupation']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter your age'}),
            'home_address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter your home address'}),
            'number_of_children': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter number of children'}),
            'date_of_last_period': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your occupation'}),
        }