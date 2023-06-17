from django import forms
from .models import EmploiDuTemps

class EmploiDuTempsForm(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = '__all__'  # Ou spécifiez les champs individuellement si nécessaire
