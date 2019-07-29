#!/usr/bin/env python
# coding: utf-8
#
#  Copyright (c) 2018-present Justin Mayer
#  Copyright (c) 2008—2016 Andy Mikhailenko
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


from _version_helper import __version__


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
    maintainer   = 'Justin Mayer',
    author_email = 'entrop@gmail.com',
    url          = 'https://github.com/justinmayer/django-autoslug/',
    download_url = 'https://github.com/justinmayer/django-autoslug/archive/master.zip',
    license      = 'GNU Lesser General Public License (LGPL), Version 3',
    keywords     = 'django field slug auto unique transliteration i18n',
    classifiers  = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
    ],
)
