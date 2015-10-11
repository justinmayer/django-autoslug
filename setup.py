#!/usr/bin/env python
# coding: utf-8
#
#  Copyright (c) 2008—2015 Andy Mikhailenko and contributors
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

import io
import os
from setuptools import setup

# A simple `from autoslug import __version__` would trigger a cascading import
# of `autoslug.fields`, then `django`.  As the latter may not be available
# (being a dependency), we try to work around it.
#
# Cases:
# 1) building the package with a global interpreter and no dependencies
#    installed globally;
# 2) installing django-autoslug before Django itself (highly unlikely).
#
# Perhaps it would be better to just change the pkg building workflow?
__version__ = None
with io.open('autoslug/__init__.py', encoding='utf8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line)
            break
assert __version__, 'autoslug.__version__ must be imported correctly'


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name     = 'django-autoslug',
    version  = __version__,
    packages = ['autoslug'],

    requires = ['python (>= 2.7)', 'django (>= 1.7.10)'],
    # in case you want to use slugify() with support for transliteration:
    extras_require = {
        'cyrillic': 'pytils >= 0.2',
        'translitcodec': 'translitcodec >= 0.3',
    },
    description  = 'An automated slug field for Django.',
    long_description = readme,
    author       = 'Andy Mikhailenko',
    author_email = 'neithere@gmail.com',
    url          = 'http://bitbucket.org/neithere/django-autoslug/',
    download_url = 'http://bitbucket.org/neithere/django-autoslug/get/tip.zip',
    license      = 'GNU Lesser General Public License (LGPL), Version 3',
    keywords     = 'django field slug auto unique transliteration i18n',
    classifiers  = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
    ],
)
