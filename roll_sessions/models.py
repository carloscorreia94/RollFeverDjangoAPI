from django.db import models
from django.forms.models import model_to_dict
from spots.models import Spot
# Create your models here.
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
        return str(model_to_dict(self))
        #for key,value in dict_model_instance.items():
         #   print("Keys: %s", value.key)
          #  print("Values: %s", value.value)