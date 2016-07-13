from __future__ import absolute_import

from celery import shared_task
from .models import WebsiteSimpleMonitor
import requests
from bs4 import BeautifulSoup
from django.db.models import ObjectDoesNotExist


website = 'http://mobile.aeist.pt/teste_changes.html'
element = 'mutant_div'
id_or_class = 'class'

@shared_task
def check_webpage():

    r = requests.get(website)
    soup = BeautifulSoup(r.text)
    contents = soup.find("div", {id_or_class: element})


    #LETS FIND THE MUTANT DIV IN THE HTML CONTENT STRING

    try:
        current_image = WebsiteSimpleMonitor.objects.get(website_url=website)
    except ObjectDoesNotExist:
        new_image = WebsiteSimpleMonitor()
        new_image.website_url = website
        new_image.website_content_div = contents
        new_image.save()

    param = "um PARAM"
    return 'The test task executed with argument "%s" ' % param


