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


class Session(models.Model):
    title = models.CharField(max_length=150,null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    # MISC Properties
    created_at = models.DateTimeField(auto_now_add=True)


    """
    Foreign Keys
    """

    # TODO: Session can be created by a group, and not only a User. Start working on groups
    created_by = models.ForeignKey('rest_auth.MyUser', on_delete=models.SET_NULL,null=True)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

    def __str__(self):
        # TODO: If title dump, creator, and main media \
        # all of it, in dictionary structure, easy to serialize
        return ""