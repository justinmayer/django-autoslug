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

"django-autoslug setup"

from distutils.core import setup
from autoslug import __version__

setup(
    name     = 'django-autoslug',
    version  = __version__,
    packages = ['autoslug'],
    
    requires = ['python (>= 2.4)', 'django (>= 1.0)'],
    # in case you want to use slugify() with support for transliteration:
    extras_require = ['pytils (>= 0.2)'],
    
    description  = 'An automated slug field for Django',
    long_description = "A slug field which can automatically a) populate itself "\
                       "from another field, b) preserve uniqueness of the value "\
                       "and c) use custom slugify() functions for better i18n.",
    author       = 'Andy Mikhailenko',
    author_email = 'andy@neithere.net',
    url          = 'http://bitbucket.org/neithere/django-autoslug/',
    download_url = 'http://bitbucket.org/neithere/django-autoslug/get/tip.zip',
    license      = 'GNU Lesser General Public License (LGPL), Version 3',
    keywords     = 'django field slug auto transliteration i18n',
)
