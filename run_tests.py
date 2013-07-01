#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
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

# django-coverage does not support Python 3 yet
if sys.version < '3.0':
    conf['INSTALLED_APPS'].append('django_coverage')
    conf.update(COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join('.', 'coverage'))
    test_command = 'test_coverage'
else:
    test_command = 'test'


settings.configure(**conf)


if __name__ == "__main__":
    call_command(test_command, 'autoslug')
