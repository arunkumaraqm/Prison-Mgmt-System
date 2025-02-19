from django.db import models

class Prisoner(models.Model):
	name = models.CharField(max_length = 100)
	start_date = models.DateTimeField(
		'start date of prison sentence',
		)

	def __str__(self): 
		return self.name

class Visitor(models.Model):
	visitor_id = models.AutoField(primary_key=True)
	visitor_name = models.CharField(max_length = 100)
	associated_prisoners = models.ManyToManyField('prison.Prisoner')

	TYPES_OF_VISITORS = {
		('L', 'Lawyer'),
		('F', 'Family or Friends'),
		('O', 'Other')
		}
	visitor_type = models.CharField(
		max_length = 1, 
		choices = TYPES_OF_VISITORS,
		default = 'O'
		) # Move this field to through

	def __str__(self): 
		return f'{self.visitor_id}: {self.visitor_name}'

