from django.db import models as md

class Prisoner(md.Model):
	name = md.CharField(max_length = 100)
	start_date = md.DateTimeField('start date of prison sentence')

