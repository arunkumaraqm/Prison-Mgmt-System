from django.db import models
from django.contrib.auth.models import AbstractUser

class Prisoner(models.Model):
	name = models.CharField(max_length = 100)
	start_date = models.DateTimeField(
		'start date of prison sentence',
		# auto_now=True
		)

	def __str__(self): 
		return self.name