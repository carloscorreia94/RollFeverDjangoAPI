from __future__ import absolute_import

from celery import shared_task

@shared_task
def check_webpage(param):
    print("hmmmm worka")
    return 'The test task executed with argument "%s" ' % param