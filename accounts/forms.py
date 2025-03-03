from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User,Location, Patient, Doctor


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
        fields = ['home_address', 'number_of_children', 'date_of_last_period', 'occupation']
        widgets = {
            'home_address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter your home address'}),
            'number_of_children': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter number of children'}),
            'date_of_last_period': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your occupation'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your old password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter new password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm new password'}),
        label="Confirm New Password"
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

class UserUpdateForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'nin', 'marital_status', 'contact']
            widgets = {
                'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter username'}),
                'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter first name'}),
                'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter last name'}),
                'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter email'}),
                'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
                'nin': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter NIN'}),
                'marital_status': forms.Select(attrs={'class': 'form-input'}),
                'contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter contact number'}),
            }

class LocationUpdateForm(forms.ModelForm):
        class Meta:
            model = Location
            fields = ['village', 'parish', 'sub_county', 'district', 'address']
            widgets = {
                'village': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter village'}),
                'parish': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter parish'}),
                'sub_county': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter sub-county'}),
                'district': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter district'}),
                'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter address'}),
            }

# forms.py
class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['home_address', 'number_of_children', 'date_of_last_period', 'occupation']
        widgets = {
            'home_address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter your home address'}),
            'number_of_children': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter number of children'}),
            'date_of_last_period': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your occupation'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['work_address', 'certificate_number', 'contact_number', 'health_facility', 'medical_field', 'experience_years', 'education_level', 'rank_title']
        widgets = {
            'work_address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter work address'}),
            'certificate_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter certificate number'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter contact number'}),
            'health_facility': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter health facility'}),
            'medical_field': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter medical field'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter years of experience'}),
            'education_level': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter education level'}),
            'rank_title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter rank/title'}),
        }
