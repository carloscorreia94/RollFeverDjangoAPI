from django.db import models
from spots.models import Spot

class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot,on_delete=models.CASCADE)