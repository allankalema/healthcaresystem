from django import forms
from .models import PreviousObstetricHistory, AntenatalProgressExamination, UltrasoundReport

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