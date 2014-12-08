"""
Django migrations for django social app

This package does not contain South migrations.  South migrations can be found
in the ``south_migrations`` package.

hat tip to Trey Hunner for this setup.
http://treyhunner.com/2014/03/migrating-to-django-1-dot-7/
"""

SOUTH_ERROR_MESSAGE = """\n
For South support, customize the SOUTH_MIGRATION_MODULES setting like so:

    SOUTH_MIGRATION_MODULES = {
        'social': 'social.south_migrations',
    }
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    from django.db import migrations  # noqa
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
