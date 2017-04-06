#!/usr/bin/env python
"""
Test runner script.

Please use `tox` to run it in multiple environments.
"""

import django
from django.conf import settings
from django.core.management import call_command


gettext = lambda s: s
conf = dict(
    LANGUAGES = (
        ('en', gettext('English')),
        ('ru', gettext('Russian')),
    ),
    LANGUAGE_CODE = 'en',
    USE_I18N = True,
    USE_TZ = False,
    INSTALLED_APPS = [
        'modeltranslation',
        'autoslug'
    ],
    MODELTRANSLATION_TRANSLATION_FILES = (
        'autoslug.tests.translations',
    ),
    DATABASES = dict(
        default = dict(
            ENGINE='django.db.backends.sqlite3',
            NAME=':memory:',
        ),
    ),
    AUTOSLUG_SLUGIFY_FUNCTION = 'django.template.defaultfilters.slugify',
    AUTOSLUG_MODELTRANSLATION_ENABLE = True,
)


settings.configure(**conf)
django.setup()

if __name__ == "__main__":
    call_command('test', 'autoslug')
