# -*- coding: utf-8 -*-

from django.conf import settings

""" the AUTOSLUG_SLUGIFY_FUNCTION setting allows to define
a custom slugifying function. Value can be a string or a callable.
Default value is 'django.template.defaultfilters.slugify'.
"""

# use custom slugifying function if any 
slugify = getattr(settings, 'AUTOSLUG_SLUGIFY_FUNCTION', None)

if not slugify:
    try:
        # more i18n-friendly slugify function (supports Russian transliteration)
        from pytils.translit import slugify
    except ImportError:
        # fall back to Django's default one
        slugify = 'django.template.defaultfilters.slugify'

# find callable by string
if isinstance(slugify, str):
    from django.core.urlresolvers import get_callable
    slugify = get_callable(slugify)
