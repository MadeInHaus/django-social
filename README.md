django-social
=============

Django app for easily including a social content api.


### install directions
    pip install -e git://github.com/MadeInHaus/django-social#egg=django-social  

add 'social' to INSTALLED_APPS in settings  

add to urls.py  

    (r'^social/', include('social.urls')),  



### Twitter
For each Twitter Search you add in, the app will try each time to start at now, and move back in time until... 
- it finds a tweet that it has in the DB
- it finds a tweet that has a timestamp that is further back in time than the search terms 'search until'
- twitters maximum number of api requests have been hit
