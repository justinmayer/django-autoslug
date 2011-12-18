#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008—2009 Andy Mikhailenko and contributors
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

import os
from setuptools import setup


readme = open(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(
    name     = 'django-autoslug',
    version  = '1.5.0',
    packages = ['autoslug'],

    requires = ['python (>= 2.4)', 'django (>= 1.0)'],
    # in case you want to use slugify() with support for transliteration:
    extras_require = {'cyrillic': 'pytils >= 0.2'},

    description  = 'An automated slug field for Django.',
    long_description = readme,
    author       = 'Andy Mikhailenko',
    author_email = 'andy@neithere.net',
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
