from django import forms
from .models import Prisoner, Visitor
from django.db.models import Q

class PrisonerForm(forms.ModelForm):
	class Meta:
		model = Prisoner 
		fields = ["name", "start_date"]

class ExistingVisitorForm(forms.Form):
	def __init__(self, applicable_visitors, *args, **kwargs):
		super(ExistingVisitorForm, self).__init__(*args, **kwargs)

		# Only show visitors that aren't already associated with the prisoner
		self.fields['visitor'] = forms.ModelChoiceField(queryset=applicable_visitors)

	# def save(self, commit=True):
	# 	# user = super().save(commit=False)
	# 	self.cleaned_data['associated_prisoners'] = 

	# 	if commit:
	# 		user.save()

	# 	return user

class NewVisitorForm(forms.ModelForm):
	class Meta:
		model = Visitor
		fields = ["visitor_name", "visitor_type"]

	def save(self, commit=True, default_associated_prisoner=None):
		if not commit:
			raise NotImplementedError("New visitor instance needs to be saved.")

		visitor = super().save()
		if default_associated_prisoner:
			visitor.associated_prisoners.add(default_associated_prisoner)
		visitor.save()
		return visitor