from .base import *  # noqa

DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

SECRET_KEY = "secret"

# DATABASE SETTINGS
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'development.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PASSING = "passing"
RUSHING = 'rushing'
RECEIVING = 'receiving'
KICKING = 'kicking'
YARDS = 'yards'
RECEPTIONS = 'receptions'
TOUCHDOWNS = 'touchdowns'
INTERCEPTIONS = 'interceptions'
FUMBLES = 'fumbles'
ONEBONUS = '100bonus'
TWOBONUS = '200bonus'
THREEBONUS = '300bonus'
FOURBONUS = '400bonus'



SCORING_SYSTEM = {
    PASSING: {
        YARDS: 0.05,
        TOUCHDOWNS: 5,
        INTERCEPTIONS: -2,
        THREEBONUS: 1,
        FOURBONUS: 2
    },
    RUSHING: {
        YARDS: 0.1,
        TOUCHDOWNS: 6,
        FUMBLES: -2,
        ONEBONUS: 1,
        TWOBONUS: 2
    },
    RECEIVING: {
        YARDS: 0.1,
        RECEPTIONS: 1,
        TOUCHDOWNS: 6,
        ONEBONUS: 1,
        TWOBONUS: 2
    },
    KICKING: {

    }
}


# DJANGO DEBUG TOOLBAR SETTINGS
# https://django-debug-toolbar.readthedocs.org
def show_toolbar(request):
    return not request.is_ajax() and request.user and request.user.is_superuser

MIDDLEWARE_CLASSES += ["debug_toolbar.middleware.DebugToolbarMiddleware", ]
INSTALLED_APPS += ["debug_toolbar", "push_notifications"]

PUSH_NOTIFICATIONS_SETTINGS = {
    "GCM_API_KEY": "<your api="" key="">",
    "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
    'TAG': 'body',
    'SHOW_TEMPLATE_CONTEXT': True,
    'ENABLE_STACKTRACES': True,
    'SHOW_TOOLBAR_CALLBACK': 'fantasy_league.settings.development.show_toolbar',
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
)

try:
    from local_settings import * # noqa
except ImportError:
    pass
