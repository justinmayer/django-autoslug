# -*- coding: utf-8 -*-

from django.conf import settings

""" the AUTOSLUGFIELD_SLUGIFY_FUNCTION setting allows to define
a custom slugifying function. Value can be a string or a callable.
Default value is 'django.template.defaultfilters.slugify'.
"""

slugify = getattr(settings, 'AUTOSLUGFIELD_SLUGIFY_FUNCTION', # use custom slugifying function...
    'django.template.defaultfilters.slugify' # ...or fall back to Django's default one
)

if isinstance(slugify, str):
    from django.core.urlresolvers import get_callable
    slugify = get_callable(slugify)
