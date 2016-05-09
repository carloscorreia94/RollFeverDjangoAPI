from django.db import models
from rest_framework.validators import UniqueValidator
from django.core import serializers

# Create your models here.

class Spot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, default='')
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    created_by = models.ForeignKey('rest_auth.MyUser', on_delete=models.SET_NULL,null=True)
    #main_pic = models.ImageField()

    def __str__(self):
        return self.name
    @staticmethod
    def nearby(lat,lng,radius):
        lname = 'Praca da Figueira'
        test = Spot.objects.raw('SELECT * FROM spots_spot WHERE name = %s', [lname])
        test = serializers.serialize('json', test, fields=('id','name','lat','lng'))
        return {'latitude':lat,'longitude':lng,'radius':radius,'test':test}
