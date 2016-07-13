from __future__ import absolute_import

from celery import shared_task
import requests

  """
    TODO: HTTP REQUEST
            FIND ELEMENT- SAVE DIV CONTENTS DATABASE


  """
website = 'http://mobile.aeist.pt/teste_changes.html'
element = 'mutant_div'

@shared_task
def check_webpage():

    r = requests.get(website)
    print(str(r))

    print("hmmmm worka")
    param = "um PARAM"
    return 'The test task executed with argument "%s" ' % param


