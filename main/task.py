
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from scrape_scheduler import settings
from datetime import datetime
from scrapI import downloader
import shutil
import os

from scrapI.s3 import download_link




# downloader.download(query_string, limit=100,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60,resize=(224,224) ,verbose=True)


# create any function/task that you want to allocate to celery
# @shared_task(bind=True)
# def test(self):
    
#     for i in range(45):
#         print(i)


       
# @shared_task(bind=True)
# def send_mail_func(self):
#     users=get_user_model().objects.all()
#     print(users)
#     for user in users:
#         mail_subject="Daily mail"
#         message='message received'
#         to_email=user.email
#         send_mail(

#             subject=mail_subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=['guptanitesh2711@gmail.com',],
#             fail_silently=True,
            

#         )
#     return 'done'

@shared_task(bind=True)
def Download_I_and_send(self,query,limit :int,resize,emails :str):
    outd=(str(datetime.now())).replace(' ','_').replace(':','_')
    output_dir=os.path.join(query+outd)
    resize=tuple([int(i) for i in resize])
    downloader.download(query, output_dir,resize,no_images=limit) 
    # shutil.make_archive('ds', 'zip', 'dataset')
    zip_d=os.path.join(output_dir)
    # zip_d is the zip dir
    shutil.make_archive(zip_d, 'zip', os.path.join(output_dir))
    # making a zip with zip_d
    url=download_link(os.path.join(zip_d+'.zip'))
    shutil.rmtree(output_dir)
    os.remove(str(zip_d)+'.zip')
    send_mail(

            subject="Images from scrapI",
            message=f'''This is the url for the images 
            {url}''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[emails,],
            fail_silently=True,
            

        )
    print('email sent')
    
    