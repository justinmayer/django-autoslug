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
from modeltranslation.translator import translator, TranslationOptions
from .models import ModeltranslationOne


class ModeltranslationOneTranslation(TranslationOptions):
    fields = ('title', 'description')


translator.register(ModeltranslationOne,
                    ModeltranslationOneTranslation)
