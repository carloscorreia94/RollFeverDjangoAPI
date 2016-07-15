from __future__ import absolute_import

from celery import shared_task
from .models import WebsiteSimpleMonitor
import requests
from bs4 import BeautifulSoup
from django.db.models import ObjectDoesNotExist

website = 'https://goo.gl/0XMmXn'
element = 'calendar-table'
id_or_class = 'class'

@shared_task
def check_webpage():
    return;
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7'}
    r = requests.get(website,headers=headers)
    soup = BeautifulSoup(r.text,"html.parser")
    contents = soup.find("div", {id_or_class: element})

    if contents is None:
        return "Didn't find what you were looking for"

    #LETS FIND THE MUTANT DIV IN THE HTML CONTENT STRING

    try:
        current_image = WebsiteSimpleMonitor.objects.get(website_url=website)

        if current_image.website_content_div != str(contents):

            current_image.website_content_div = str(contents)
            current_image.save()
            return WebsiteSimpleMonitor.send_email("carloscorreia94@gmail.com")
        return "same bouullsheit"

    except ObjectDoesNotExist:
        new_image = WebsiteSimpleMonitor()
        new_image.website_url = website
        new_image.website_content_div = str(contents)
        new_image.save()

    param = "um PARAM"
    return 'The test task executed with argument "%s" ' % param


