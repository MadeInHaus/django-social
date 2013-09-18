## Frontend Dev notes ##


Haus boilerplate enables [django-require](http://github.com/etianen/django-require) which automatically runs the JS compile process when you run a collect static.
To test this run the following:


    fab vagrant.collectstatic

This process will compile all of the Javascript with the [r.js](http://github.com/jrburke/r.js) optimizer as set up in your [build profile](http://requirejs.org/docs/optimization.html#wholeproject).
Your build profile should be located at `project/static/js/app.build.js`

To toggle the build process while developing, create a file at `project/settings/hosts/local_settings.py`
**This file will alter your env compared to the other developers.**

Inside `local_settings.py` add:
    
    from settings import *
    import sys
    print >> sys.stderr, "**Using Local Settings**"
    # False = Do not serve project/static/
    DEBUG = False
    # True = server collected-static/
    SERVE_STATIC = True

Keep in mind, to have the application pull the uncompiled files, you need to flip those variables to the inverse.  
