"""
Django settings for music_planner0 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import DEFAULT_FILE_STORAGE
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1)!!b1c-(apmbv15!j8+0(!p2evpm0#o7izhx-q4n-#e4cmaul'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

td = False
tdir = []


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True


CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['*']

has_openshift = 'OPENSHIFT_HOMEDIR' in os.environ
#webfaction = 'HOSTNAME' in os.environ and 'webfaction' in os.environ['HOSTNAME']
webfaction = '_' in os.environ
#print (os.environ)
# Application definition
if webfaction:
    print ("webfaction detected")
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'unix:/home/jchinte/memcached.sock',
        }
    }
    print(CACHES)
else:
    print ("webfaction not detected")
INSTALLED_APPS = (
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SongManager',
    'Event_Planner.apps.Event_PlannerConfig',
    'dh5bp',
    'dh5mbp',
    'django_mobile',
    'django.contrib.sites'
)

MIDDLEWARE_CLASSES = (
    #'ssl_redirect.middleware.SSLRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'music_planner0.urls'

WSGI_APPLICATION = 'music_planner0.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'praisingvoices_postgres',
        'USER': 'pvdb',
        'PASSWORD': 'liltheo1025',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'praisingvoices_postgres',
        'USER': 'pvdb',
        'PASSWORD': 'liltheo1025',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            }, 
        'NAME': 'choirplanner',
        'USER': 'choirplanner',
        'PASSWORD': 'choirplanner',
        'HOST': '127.0.0.1',
        },
}
if not webfaction:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db2.sqlite3'),
        },
    }
    CSRF_COOKIE_SECURE = False
STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )
STATIC_ROOT= os.path.join(BASE_DIR, '../../praisingvoices_static/static')
MEDIA_ROOT = os.path.join(BASE_DIR, '../../praisingvoices_static/media')
#MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    '/home/jchinte/webapps/praisingvoices_static/static' if webfaction else '/Users/jchinte/webapps/praisingvoices_static/static',
    )
print(STATIC_ROOT)
tdir = [os.path.join(BASE_DIR, 'templates'),]
DEBUG = True
td = True
SITE_ID=2
JAVA_GATEWAY_ADDRESS = '127.0.0.1'

JAVA_DIR = os.path.join(BASE_DIR,  'lib')
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/





#MEDIAFILES_DIRS = (
#                   os.path.join(BASE_DIR, "media"),
#                   '/home/jchinte/code/media/')



SERIALIZATION_MODULES = {
                         'json': 'wadofstuff.django.serializers.json2' 
                         }
LOGIN_REDIRECT_URL='/events/'
LOGIN_URL='/accounts/login'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': tdir,
        'OPTIONS': {
            'debug': td,
            'context_processors': [ 
                "django.contrib.auth.context_processors.auth",
                #"django.core.context_processors.debug",
                #"django.core.context_processors.i18n",
                #"django.core.context_processors.media",
                #"django.core.context_processors.static",
                #"django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                #'django.core.context_processors.request',
                'django_mobile.context_processors.flavour',                                
                'context_processors.dh5mbp_jquery_mobile',
            ],
            'loaders': [
                'django_mobile.loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',

                
            ]
        },
    },
]
#django-mobile hack
TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']
EMAIL_HOST='smtp.webfaction.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='jchinte'
EMAIL_HOST_PASSWORD='>vRDcEBu+H@L%7?v'
DEFAULT_FROM_EMAIL='praisingvoices@praisingvoices.org'
SERVER_EMAIL='praisingvoices@praisingvoices.org'
ACCOUNT_ACTIVATION_DAYS=7
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_ADMINS=[('jchinte','jchinte@gmail.com'),]
REGISTRATION_FORM='registration_pv.forms.PVRegistrationForm'
ADMINS=[('jchinte','jchinte@gmail.com'),]
FILE_UPLOAD_PERMISSIONS=0o644
