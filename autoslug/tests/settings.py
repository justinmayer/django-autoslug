"""Django test settings for django-autoslug.

Mirrors the configuration previously defined inline in run_tests.py.
"""


def gettext(s):
    return s


LANGUAGES = (
    ("ru", gettext("Russian")),
    ("en", gettext("English")),
)

USE_TZ = False

INSTALLED_APPS = [
    "modeltranslation",
    "autoslug",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

AUTOSLUG_SLUGIFY_FUNCTION = "django.template.defaultfilters.slugify"
