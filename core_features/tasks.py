from __future__ import absolute_import

from celery import shared_task
from .models import WebsiteSimpleMonitor
import requests
from bs4 import BeautifulSoup
from django.db.models import ObjectDoesNotExist


website = 'https://service.berlin.de/terminvereinbarung/termin/tag.php?id=&buergerID&buergername=&absagecode=&Datum=1467324000&anliegen[]=120335&dienstleister[]=327316&dienstleister[]=327312&dienstleister[]=327314&dienstleister[]=327346&dienstleister[]=327423&dienstleister[]=327348&dienstleister[]=122252&dienstleister[]=327338&dienstleister[]=122260&dienstleister[]=327340&dienstleister[]=122262&dienstleister[]=122254&dienstleister[]=327278&dienstleister[]=327274&dienstleister[]=327276&dienstleister[]=327294&dienstleister[]=327290&dienstleister[]=327292&dienstleister[]=122291&dienstleister[]=327270&dienstleister[]=122285&dienstleister[]=327266&dienstleister[]=122286&dienstleister[]=327264&dienstleister[]=122296&dienstleister[]=327268&dienstleister[]=150230&dienstleister[]=327282&dienstleister[]=327286&dienstleister[]=327284&dienstleister[]=122312&dienstleister[]=122314&dienstleister[]=122304&dienstleister[]=327330&dienstleister[]=122311&dienstleister[]=327334&dienstleister[]=122309&dienstleister[]=327332&dienstleister[]=317869&dienstleister[]=325341&dienstleister[]=324434&dienstleister[]=327352&dienstleister[]=122283&dienstleister[]=327354&dienstleister[]=122276&dienstleister[]=327324&dienstleister[]=122274&dienstleister[]=327326&dienstleister[]=122267&dienstleister[]=327328&dienstleister[]=122246&dienstleister[]=327318&dienstleister[]=122251&dienstleister[]=327320&dienstleister[]=122257&dienstleister[]=327322&dienstleister[]=122208&dienstleister[]=327298&dienstleister[]=122226&dienstleister[]=327300&herkunft=http://service.berlin.de/dienstleistung/120335/standort/327346/'
element = 'calendar-table'
id_or_class = 'class'

@shared_task
def check_webpage():

    r = requests.get(website)
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


