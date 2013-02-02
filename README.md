django-social
=============

Django app for easily including a social content api.


### Twitter
For each Twitter Search you add in, the app will try each time to start at now, and move back in time until... 
1. it finds a tweet that it has in the DB
1. it finds a tweet that has a timestamp that is further back in time than the search terms 'search until'
1. twitters maximum number of api requests have been hit
