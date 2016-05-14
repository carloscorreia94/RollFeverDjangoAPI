from django.db import models
from rest_framework.validators import UniqueValidator
from django.core import serializers
from rollfeverapi.common import upload_utils
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class Spot(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, default='')
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    created_by = models.ForeignKey('rest_auth.MyUser', on_delete=models.SET_NULL,null=True)

    # TODO : Take care of max size (width,height) here - vs client side
    main_pic = models.ImageField(upload_to=upload_utils.PathAndRename('rollfeverapi/static/uploads/spots/main_pics/'), null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Spot, self).save(*args, **kwargs)
        thermo = Thermometer()
        thermo.spot = self
        thermo.save()

class Thermometer(models.Model):
    reputation = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    flatground = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    people = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    spot = models.ForeignKey(Spot,on_delete=models.CASCADE)