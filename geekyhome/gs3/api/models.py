from django.db import models
from django.forms import CharField
from numpy import True_

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(blank=True)
    city = models.CharField(max_length=100)