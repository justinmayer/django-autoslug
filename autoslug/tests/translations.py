from modeltranslation.translator import translator, TranslationOptions
from .models import ModeltranslationOne, ModeltranslationWithoutSlug, ModeltranslationWithSlug


class ModeltranslationOneTranslation(TranslationOptions):
    fields = ('title', 'description', )


translator.register(ModeltranslationOne,
                    ModeltranslationOneTranslation)


class ModeltranslationWithoutSlugTranslation(TranslationOptions):
    fields = ('title', )


translator.register(ModeltranslationWithoutSlug,
                    ModeltranslationWithoutSlugTranslation)


class ModeltranslationWithSlugTranslation(TranslationOptions):
    fields = ('title', 'slug', )


translator.register(ModeltranslationWithSlug,
                    ModeltranslationWithSlugTranslation)

