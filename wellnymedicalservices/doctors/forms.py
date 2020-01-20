from django import forms
from .models import Diagnosis, TODOItem


class DiagnosisForm(forms.ModelForm):

    class Meta:
        model = Diagnosis
        fields = ['name', 'Rostered_physician', 'condition', 'details', 'date_of_diagnosis', 'content']


class TODOItemForm(forms.ModelForm):

    class Meta:
        model = TODOItem
        fields = ['job', 'due_date', 'medication_details', 'completed']


