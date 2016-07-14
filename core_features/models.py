from django.db import models
from django.db.models import ObjectDoesNotExist
# Create your models here.


class PendingMedia(models.Model):
    pending_media_number = models.IntegerField()
    media_type = models.CharField(max_length=100)
    content_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def add_pending_media(media_number, media_type, content_id):
        pending_media = PendingMedia()
        pending_media.pending_media_number = media_number
        pending_media.media_type = media_type
        pending_media.content_id = content_id
        pending_media.save()


    @staticmethod
    def media_to_wait(media_type):
        return PendingMedia.objects.filter(media_type=media_type, pending_media_number__gt=0).values_list('content_id')

    @staticmethod
    def update_pending_media(media_type,content_id,media_number):
        try:
            pending_media_item = PendingMedia.objects.get(media_type=media_type,content_id=content_id)
            if pending_media_item.pending_media_number == 1 or pending_media_item.pending_media_number - media_number < 1:
                pending_media_item.delete()
            pending_media_item.pending_media_number -= media_number
            pending_media_item.save()
            return True
        except ObjectDoesNotExist:
            return False

class WebsiteSimpleMonitor(models.Model):
    website_url = models.CharField(max_length=300)
    website_content_div = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def send_email(email_address):
        from django.core.mail import send_mail
        send_mail(
            'SpotMania DJANGO',
            'BORA _ Registares te',
            'spotmania@aeist.pt',
            [email_address],
            fail_silently=False,
        )
        return "I've just sent email to this folk's address - %s" % email_address