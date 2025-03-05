from django import forms
from .models import *
from accounts.models import *

class AntenatalCardForm(forms.ModelForm):
    class Meta:
        model = AntenatalCard
        fields = [
            'health_unit', 'reg_no', 'nin', 'phone_no', 'age', 'village', 'parish', 'sub_county', 'district',
            'occupation', 'religion', 'education_level', 'tribe', 'marital_status', 'next_of_kin_name',
            'next_of_kin_phone', 'next_of_kin_relationship', 'next_of_kin_address', 'gravida', 'para', 'abortions',
            'presenting_complaints', 'first_day_of_lnmp', 'edd', 'weeks_of_amenorrhea', 'complications_of_pregnancy',
            'hospitalization', 'hospitalization_reason', 'next_visit'
        ]
        widgets = {
            'nin': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'age': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'village': forms.TextInput(attrs={'readonly': 'readonly'}),
            'parish': forms.TextInput(attrs={'readonly': 'readonly'}),
            'sub_county': forms.TextInput(attrs={'readonly': 'readonly'}),
            'district': forms.TextInput(attrs={'readonly': 'readonly'}),
            'occupation': forms.TextInput(attrs={'readonly': 'readonly'}),
            'marital_status': forms.Select(attrs={'readonly': 'readonly'}),
        }