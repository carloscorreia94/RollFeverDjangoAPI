from django.db import models
from django.db.models import Manager
from rest_framework.validators import UniqueValidator
from django.core import serializers
from spotmaniaapi.common import upload_utils
from django.core.validators import MaxValueValidator,MinValueValidator
from core_features.models import PendingMedia

# Create your models here.


class SpotObjectManager(models.Manager):
    def get_queryset(self):
        pending_media_results = PendingMedia.media_to_wait(Spot.MEDIA_TYPE)
        query = super(SpotObjectManager,self).get_queryset().filter().exclude(id__in=pending_media_results).distinct()
        return query


class Spot(models.Model):

    MEDIA_TYPE = "user_created_spot"

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    created_by = models.ForeignKey('rest_auth.MyUser', on_delete=models.SET_NULL,null=True)

    # TODO : Take care of max size (width,height) here - vs client side
    main_pic = models.ImageField(upload_to=upload_utils.PathAndRename('spots/main_pics/'), null=True)

    #objects = SpotObjectManager()
    all_objects = Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        create = self.pk is None
        super(Spot, self).save(*args, **kwargs)

        if create:
            PendingMedia.add_pending_media(1, Spot.MEDIA_TYPE, self.id)

           # thermo = Thermometer()
           # thermo.spot = self
           # thermo.save()


#class Thermometer(models.Model):
#    reputation = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
#    flatground = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
#    people = models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
#    spot = models.ForeignKey(Spot,on_delete=models.CASCADE)
