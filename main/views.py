import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from scrape_scheduler import settings
from django_celery_beat.models import PeriodicTask,CrontabSchedule
import logging
import os
logging_str='[%(asctime)s: %(levelname)s: %(module)s]: %(message)s'


logging.basicConfig(filename=os.path.join('load_data.log'),level=logging.INFO,format=logging_str,filemode='a')

from datetime import datetime


# Create your views here.




def hourU(num):
    # converts IST to UTC
    num=num-5
    if num<=0:
        return 24-abs(num)
    else: return num
def minuteU(num):
    num=num-30
    if num<=0:
        return 60-abs(num)
    else:return num



def testA(request):
    if request.method=="GET":
    
    # above is a celery task
        logging.info('get request made to the scrapper')
        return render(request,'index.html')


def schedule(request):
    if request.method=="POST":
        #func.delay()
        # import func
        logging.info('Post request received')
        imagename=request.POST.get('Image_Query')
        
        limit=request.POST.get('Limit')
        height=request.POST.get('Height')
        width=request.POST.get('Width')
        email=request.POST.get('email')
        time=request.POST.get('time')
        space="  "
        logging.info('all the parameters received query,limit height etc')
        
        context={"imagename":imagename,"limit":limit,"email":email,"time":time,"space":space}
        tt=time.split(':')
        hour=int(tt[0])
        minute=int(tt[1])
        logging.info('prpared to add to Django ORM schedular')
        #tup=tuple([int(i) for i in [height,width]])
        scheduleT,created=CrontabSchedule.objects.get_or_create(hour=hour,minute=minute)
        uname=imagename+(str(datetime.now())).replace(' ','_').replace(':','_')
        task=PeriodicTask.objects.create(crontab=scheduleT,name=uname,task='main.task.Download_I_and_send',args=json.dumps((str(imagename),int(limit),(height,width),str(email))))
        logging.info(f'schedule task from user has been added at {time } for {imagename} for {limit} images')

        



        return render(request,'end.html',context)




# def mailing(request):
#     send_mail_func.delay()
#     return HttpResponse('Done mail sended')


# dynamically adding tasks to django-celery beat
# def add_task(request):
#     scheduleT,created=CrontabSchedule.objects.get_or_create(hour=1,minute=2)
#     task=PeriodicTask.objects.create(crontab=scheduleT,name='unique_name',task='main.task.send_mail_func',args=json.dumps(('args')))

#     return HttpResponse('Done')
