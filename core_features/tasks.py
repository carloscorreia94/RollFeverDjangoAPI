from __future__ import absolute_import

from celery import shared_task

@shared_task
def check_webpage():
    print("hmmmm worka")
    param = "um PARAM"
    return 'The test task executed with argument "%s" ' % param