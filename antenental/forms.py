from django import forms
from .models import PreviousObstetricHistory, AntenatalProgressExamination, UltrasoundReport, AntenatalCard

class PreviousObstetricHistoryForm(forms.ModelForm):
    class Meta:
        model = PreviousObstetricHistory
        fields = '__all__'
        exclude = ['antenatal_card', 'recorded_by']

class AntenatalProgressExaminationForm(forms.ModelForm):
    class Meta:
        model = AntenatalProgressExamination
        fields = '__all__'
        exclude = ['antenatal_card', 'recorded_by']

class UltrasoundReportForm(forms.ModelForm):
    class Meta:
        model = UltrasoundReport
        fields = '__all__'
        exclude = ['antenatal_card', 'recorded_by']

class AntenatalCardUpdateForm(forms.ModelForm):
    class Meta:
        model = AntenatalCard
        fields = ['next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_relationship', 'next_of_kin_address']