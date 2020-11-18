from django import forms
from .models import Prisoner as Pr, Visitor

class PrisonerForm(forms.ModelForm):
	class Meta:
		model = Pr 
		fields = ["name", "start_date"]

class VisitorForm(forms.ModelForm):
	class Meta:
		model = Visitor
		fields = "__all__"

	# def save(self, commit=True):
 #        # user = super().save(commit=False)
 #        print("LOG", self.cleaned_data['visitor_id'])

 #        if commit:
 #            user.save()

 #        return user
