# Deployment Notes

Here is where deployment instructions will go.

Should be a simple command to deploy to dev/stage/prod on heroku.

Eventually other standard platform deployments could also go here.

Project specific instructions would be included in this file as well.

-----

# Heroku quick start
- install the heroku app, if not already installed
- add all of the resources and commit to your git repo.  
- Then create the heroku app, 
- setup the APP_ENV to heroku to use the heroku.py settings file, alternativly this file could be copied to production.py and APP_ENV=production etc.
- create a dev db (or provision a larger db as necessary
- promote db to be default
- deploy to heroku
- syncdb (this step will require creation of an admin user)
- page should serve

```
git add .
git commit -a -m 'initial commit'
heroku create app-name
heroku config:set APP_ENV=heroku
heroku addons:add heroku-postgresql:dev
heroku pg:promote HEROKU_POSTGRESQL_(use result from last command)
git push heroku master
heroku run ./manage.py syncdb
heroku open
```