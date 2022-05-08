from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','scrape_scheduler.settings')
app=Celery('scrape_scheduler',include=['main.task',])
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')






#   celery Beat Settings
# app.conf.beat_schedule={
#   'send-mail-every-day-at-8':{
#     'task':'main.task.send_mail_func',
#     'schedule':crontab(hour=0,minute=46,),
#     #'args':()


    #   }}


    




app.autodiscover_tasks()






@app.task(bind=True)
def debug_task(self):
    print(f'Request : {self.request!r}')
