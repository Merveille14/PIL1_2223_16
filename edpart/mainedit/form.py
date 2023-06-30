from django import forms
from .models import Semes

class SemesForm(forms.ModelForm):
    class Meta:
        model = Semes
        fields = '__all__'