from django.contrib import admin

# Register your models here.
from .models import Prisoner as Pr
admin.site.register(Pr)