#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2009 Andy Mikhailenko and contributors
#
#  This file is part of Django AutoSlugField.
#
#  Django LJSync is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

" Django AutoSlugField setup "

from distutils.core import setup
from autoslugfield import __version__

setup(
    name     = 'django-autoslugfield',
    version  = __version__,
    packages = ['autoslugfield'],
    
    install_requires = ['python >= 2.4', 'django >= 1.0', 'pytils >= 0.2'],
    
    description  = 'An automated slug field for Django',
    long_description = "A slug field which can automatically a) populate itself from another field, and b) preserve uniqueness of the value.",
    author       = 'Andy Mikhailenko',
    author_email = 'neithere@gmail.com',
    url          = 'http://bitbucket.org/neithere/django-autoslugfield/',
    download_url = 'http://bitbucket.org/neithere/django-autoslugfield/get/tip.zip',
    license      = 'GNU Lesser General Public License (LGPL), Version 3',
    keywords     = 'django field slug transliteration i18n',
)
