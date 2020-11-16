from django import forms
from .models import Prisoner as Pr 

class PrisonerForm(forms.ModelForm):
	class Meta:
		model = Pr 
		fields = ["name", "start_date"]
