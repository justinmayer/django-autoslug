#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management import call_command


settings.configure(
    INSTALLED_APPS=('autoslug', 'django_coverage'),
    DATABASE_ENGINE='sqlite3',
    AUTOSLUG_SLUGIFY_FUNCTION='django.template.defaultfilters.slugify',
    COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join('.', 'coverage')
)

if __name__ == "__main__":
    call_command('test_coverage', 'autoslug')
