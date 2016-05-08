from django.db import models
from rest_framework.validators import UniqueValidator

# Create your models here.

class Spot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, default='')
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    #created_by = models.ForeignKey('user')
    #main_pic = models.ImageField()