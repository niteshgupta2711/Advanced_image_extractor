from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('',views.testA,name='tests'),
    path('schedule/',views.schedule,name='Scheduling'),
    
]
 #path('sendmail/',views.mailing,name='mailing'),