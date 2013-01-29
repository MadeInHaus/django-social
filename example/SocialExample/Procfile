web: python manage.py collectstatic --noinput; gunicorn project.wsgi -b 0.0.0.0:$PORT -k gevent -w 3
celeryd: python manage.py celeryd -E -B --loglevel=INFO

