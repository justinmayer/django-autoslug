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


from django.db.models import Model, CharField
from autoslug.fields import AutoSlugField


class Foo(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)

class ModelWithCustomPrimaryKey(Model):
    custom_primary_key = CharField(primary_key=True, max_length=1)
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)

__doc__ = """
>>> long_name = 'x' * 250
>>> foo = Foo(name=long_name)
>>> foo.save()
>>> len(foo.slug)
50
>>> bar = Foo(name=long_name)
>>> bar.save()
>>> [len(x.slug) for x in Foo.objects.all()]
[50, 50]

# Models with custom primary keys should work
>>> first_model_instance = ModelWithCustomPrimaryKey.objects.create(custom_primary_key='a', name='name used in slug')
>>> second_model_instance = ModelWithCustomPrimaryKey.objects.create(custom_primary_key='b', name='name used in slug')

"""
