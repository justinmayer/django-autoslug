from modeltranslation.translator import translator, TranslationOptions
from .models import ModeltranslationOne


class ModeltranslationOneTranslation(TranslationOptions):
    fields = ('title', 'description')


translator.register(ModeltranslationOne,
                    ModeltranslationOneTranslation)

