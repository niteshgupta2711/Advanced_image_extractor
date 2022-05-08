```python env
 --->   conda create --prefix ./sch python=3.7 -y
 --->   activate the env
 ```
 ```python env
 --->   pip install django
 ```

 ```python env
 --->   django-admin startproject scrape_scheduler
 ```
 ```python env
 --->   pip install celery
 ```
 ```python env
 --->   making modifiction to settings.py
 ```
 ```python env
 --->   django-admin startapp main
 ```
 ```python env
 --->   install redis on linux
 ```
 ```python env
 --->   think of celery as a worker which will do all the tasks instead of django
 ```
 ```python env
 --->   once the settings in project folder is modified to clery configs
 ```
 ```python env
 --->   create a celery.py in project folder
 ```
 ```python env
 --->   create a task.py in main folder
 ```
 ```python env
 --->   pip install redis
 ----> project folder urls will redirect you to application
 ----> application have their own urls.py 
 ```

 ''' start the djnago server and then in new terminal
   celery -A project_name.celery worker --pool=solo -l info''' for windows / linux remove --pool=solo

''' pip install django-celery'''
 # add all your apps in settings.py
 ''' every time you add apps in settings.py 
 run python manage.py makemigrations
  python manage.py migrate
  ######### run all the above in linux before getting any started
  ## even the task has not been completed return will be done from django and celery runs the task parallely

# python manage.py createsuperuser 
# checkout the /admin you will see your tasks there
# schedule beat is used to perform schedule task or say periodic 
# pip install django-celery-beat
# celery -A scrape_scheduler beat -l info
 ###-------->
 # a broker acts as a intermiatery which allows communications from django to workers\
 # this broker can be redis ,rabbitmq etc
 # celery -A project.celery worker --pool=prefork (pool of child precesses) --concurrency=5(threads by default it is no of cores in cpu) --autoscale=10,3 -l info
 # Using Django_ORM to dynamically allocate tasks to django-celery-beat