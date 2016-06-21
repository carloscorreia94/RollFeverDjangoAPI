from django.db import models

# Create your models here.


class PendingMedia(models.Model):
    media_number = models.IntegerField()
    media_type = models.CharField(max_length=100)
    content_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def add_pending_media(media_number, media_type, content_id):
        pending_media = PendingMedia()
        pending_media.media_number = media_number
        pending_media.media_type = media_type
        pending_media.content_id = content_id
        pending_media.save()


    @staticmethod
    def media_to_wait(media_type):
        #TODO: FILTER OBJECTS WITH PENDING MEDIA MORE THAN 0!!!!
        return PendingMedia.objects.filter(media_type=media_type).values_list('content_id')