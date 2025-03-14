from django import forms
from .models import *
from django.forms import formset_factory

class PreviousObstetricHistoryForm(forms.ModelForm):
    class Meta:
        model = PreviousObstetricHistory
        fields = '__all__'
        exclude = ['antenatal_card', 'recorded_by','created_at']

class AntenatalProgressExaminationForm(forms.ModelForm):
    class Meta:
        model = AntenatalProgressExamination
        fields = '__all__'
        exclude = ['antenatal_card', 'recorded_by','created_at']

class UltrasoundReportForm(forms.ModelForm):
    class Meta:
        model = UltrasoundReport
        fields = '__all__'
        exclude = ['antenatal_card', 'recorded_by','created_at']

class AntenatalCardUpdateForm(forms.ModelForm):
    class Meta:
        model = AntenatalCard
        fields = ['next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_relationship', 'next_of_kin_address']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['disease_condition', 'extra_information']
        widgets = {
            'disease_condition': forms.TextInput(attrs={'class': 'form-input'}),
            'extra_information': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medication_name', 'dosage']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-input'}),
            'dosage': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }

# Create a formset for medications
MedicationFormSet = formset_factory(MedicationForm, extra=1)


class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['emergency_type', 'description']
        widgets = {
            'emergency_type': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }