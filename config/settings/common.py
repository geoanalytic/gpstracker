# -*- coding: utf-8 -*-
"""
Django settings for Cookie Cutter Demo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (cookie_cutter_demo/config/settings/common.py - 3 = cookie_cutter_demo/)
APPS_DIR = ROOT_DIR.path('cookie_cutter_demo')

env = environ.Env()
env.read_env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'leaflet', # django-leaflet
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    'cookie_cutter_demo.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'geodata',
    'geobase',
    'rigstreet',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'cookie_cutter_demo.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)
# DEBUG = True

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""David Currie""", 'dcurrie@geoanalytic.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///cookie_cutter_demo'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
# specify Postgis backend 
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Edmonton'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'cookie_cutter_demo.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'cookie_cutter_demo.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
# Settings for Django-leaflet -- see https://github.com/makinacorpus/django-leaflet
LEAFLET_CONFIG = {
#    'SPATIAL_EXTENT': (-121, 48, -109, 61),  # Limits the panning
    'DEFAULT_CENTER': (54.5, -115),           # Not as good as SPATIAL_EXTENT since extent varies with brower size
    'DEFAULT_ZOOM': 5,						  #  good for a phone
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 21,
    'TILES': [('OpenStreetMap', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>', 'maxZoom': 19}),
              ('Toner', 'http://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png', {'attribution': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' +
					'<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; ' +
					'Map data {attribution.OpenStreetMap}','maxZoom': 20 }),
			  ('Terrain', 'http://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png', {'attribution': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' +
					'<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; ' +
					'Map data {attribution.OpenStreetMap}','maxZoom': 18 })
					],
    'OVERLAYS': [
				('NTS Index',      'https://webmap.positionbot.com/mapcache/tms/1.0.0/NTS@g21/{z}/{x}/{y}.png',    {'attribution': 'Data from <a href="http://www.GeoAnalytic.com">GeoAnalytic</a>','maxZoom': 21, 'tms': 'true' }),
				('Township System',      'https://webmap.positionbot.com/mapcache/tms/1.0.0/DLS@g21/{z}/{x}/{y}.png',    {'attribution': 'Data from <a href="http://altalis.com">AltaLIS</a>','maxZoom': 21, 'tms': 'true' }),
				('Quickbird 2012', 'https://webmap.positionbot.com/mapcache/tms/1.0.0/Quickbird_2012@g/{z}/{x}/{y}.png', {'attribution': 'Image data by <a href="http://digitalglobe.com">DigitalGlobe</a>','maxZoom': 18, 'tms': 'true' }),
				('Quickbird 2015', 'https://webmap.positionbot.com/mapcache/tms/1.0.0/Quickbird_2015@g/{z}/{x}/{y}.png', {'attribution': 'Image data by <a href="http://digitalglobe.com">DigitalGlobe</a>','maxZoom': 18, 'tms': 'true' }),
				('Cadastral',      'https://webmap.positionbot.com/mapcache/tms/1.0.0/Cadastral@g21/{z}/{x}/{y}.png',    {'attribution': 'Data from <a href="http://altalis.com">AltaLIS</a>','maxZoom': 21, 'tms': 'true' }),
				('Basemap',        'https://webmap.positionbot.com/mapcache/tms/1.0.0/AltaLIS_20k@g/{z}/{x}/{y}.png',    {'attribution': 'Data from <a href="http://altalis.com">AltaLIS</a>','maxZoom': 18, 'tms': 'true' })
					],
          
    'SCALE': 'both',
    'ATTRIBUTION_PREFIX': 'Powered by django-leaflet',
    'MINIMAP': True,
	'RESET_VIEW' : False,
#    'NO_GLOBALS' : False,
	'PLUGINS': {
		'MousePosition': {
			'css':'/static/css/L.Control.MousePosition.css',
			'js': '/static/js/L.Control.MousePosition.js',
			'auto-include': True,
		},
		
# https://gist.github.com/alfredotranchedone/72326145ecff5d7d7233
		'BetterWMS': {
			'js': '/static/js/L.TileLayer.BetterWMS.js',
			'auto-include': True,
		},
		
# https://github.com/gmaclennan/leaflet-bing-layer
		'bing': {
			'js': '/static/js/leaflet-bing-layer.js',
			'auto-include': True,
		},
	},
}
