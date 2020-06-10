from django.db import models

# Create your models here.

class Company(models.Model) :
    ticker = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)