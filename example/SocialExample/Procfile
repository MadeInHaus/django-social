web: newrelic-admin run-program python manage.py run_gunicorn project.wsgi -b 0.0.0.0:$PORT -k gevent -w 9
celeryd: newrelic-admin run-program python manage.py celeryd -E -B --loglevel=INFO
