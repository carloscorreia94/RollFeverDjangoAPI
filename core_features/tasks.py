from __future__ import absolute_import

from celery import shared_task
from .models import WebsiteSimpleMonitor
import requests
from django.db.models import ObjectDoesNotExist


website = 'http://mobile.aeist.pt/teste_changes.html'
element = 'mutant_div'

@shared_task
def check_webpage():

    r = requests.get(website)

    try:
        current_image = WebsiteSimpleMonitor.objects.get(website_url=website)
    except ObjectDoesNotExist:
        new_image = WebsiteSimpleMonitor()
        new_image.website_url = website
        new_image.website_content_div = r.text

    print(str(r))

    print("hmmmm worka")
    param = "um PARAM"
    return 'The test task executed with argument "%s" ' % param


