Project settings
================================================

How settings are loaded
-----------------------------

The base.py settings file contains the default settings. Those settings can then be overiden by modules in the hosts directory. Your options are:

1) If you specifiy a module to import with a environment varible.

    PROJECT_OVERRIDE = 'test'
    export PROJECT_OVERRIDE

Then that module will be imported from the hosts directory

2) If there is a module named 'local_settings' in your hosts directory then that will be imported

3) If there is a module named after the first part of your computer name in your hosts directory then it will be imported. For example if your computer name is web.local then if there is a file web.py in your hosts directory it will be used.

Any code that you want to run after the settings have been finalized should go the __init__.py file. See the logging setup for an example.
