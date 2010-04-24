# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008—2009 Andy Mikhailenko
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

from django.conf import settings

__doc__ = """Available settings for django-autoslug:

* `AUTOSLUG_SLUGIFY_FUNCTION` allows to define a custom slugifying function.

  The function can be repsesented as string or callable, e.g.::

      # custom function, path as string:
      AUTOSLUG_SLUGIFY_FUNCTION = 'some_app.slugify_func'

      # custom function, callable:
      AUTOSLUG_SLUGIFY_FUNCTION = some_app.slugify_func

      # custom function, defined inline:
      AUTOSLUG_SLUGIFY_FUNCTION = lambda slug: 'can i haz %s?' % slug

  Default value is 'django.template.defaultfilters.slugify' or,
  pytils.translit's slugify function if installed.
"""

# use custom slugifying function if any
slugify = getattr(settings, 'AUTOSLUG_SLUGIFY_FUNCTION', None)

if not slugify:
    try:
        # i18n-friendly approach
        from unidecode import unidecode
        slugify = lambda s: unidecode(s).replace(' ', '-')
    except ImportError:
        try:
            # Cyrillic transliteration (primarily Russian)
            from pytils.translit import slugify
        except ImportError:
            # fall back to Django's default method
            slugify = 'django.template.defaultfilters.slugify'

# find callable by string
if isinstance(slugify, str):
    from django.core.urlresolvers import get_callable
    slugify = get_callable(slugify)
