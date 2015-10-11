#!/usr/bin/env python
"""
Test runner script.

Please use `tox` to run it in multiple environments.
"""

import django
from django.conf import settings
from django.core.management import call_command


conf = dict(
    INSTALLED_APPS = ['autoslug'],
    DATABASES = dict(
        default = dict(
            ENGINE='django.db.backends.sqlite3',
        ),
    ),
    AUTOSLUG_SLUGIFY_FUNCTION = 'django.template.defaultfilters.slugify',
)


settings.configure(**conf)
django.setup()

if __name__ == "__main__":
    call_command('test', 'autoslug')
