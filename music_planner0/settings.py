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

ALLOWED_HOSTS = ['*']

has_openshift = 'OPENSHIFT_HOMEDIR' in os.environ

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SongManager',
    'Event_Planner.apps.Event_PlannerConfig',
    'registration',
    'dh5bp',
    'dh5mbp',
    'django_mobile',
    'django.contrib.sites'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)

ROOT_URLCONF = 'music_planner0.urls'

WSGI_APPLICATION = 'music_planner0.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if has_openshift:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                    #'read_default_file': '/webapps/musicplanner0/svn/music_planner0/my.cnf'
                     # 'read_default_file': os.environ['OPENSHIFT_HOMEDIR']+'/my.cnf'
                    },
            'NAME': 'choirplanner',
            'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
            'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
            'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
        }
    }
    STATIC_URL = '/static/'
    MEDIA_URL = '/static/data/'
    STATICFILES_DIRS = (
                    os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'wsgi','static'))
    JAVA_GATEWAY_ADDRESS = os.environ['OPENSHIFT_JAVAGATEWAY_JAVAGATEWAY_IP']
    STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'wsgi','static')
    MEDIA_ROOT = os.environ['OPENSHIFT_DATA_DIR']
    tdir = [os.path.join(os.environ['OPENSHIFT_REPO_DIR'],'templates')]
    SITE_ID = 2
elif os.getenv('SERVER_SOFTWARE','').startswith('Google App Engine'):
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = 'choirplanner-media'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/elemental-kite-178117:us-west1:choirplanner-normal',
            'NAME': 'choirplanner',
            'USER': 'choirplanner',
            'PASSWORD': 'choirplanner'
        }
    }
    STATIC_URL = '/static/static/'
    MEDIA_URL = '/static/media/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
        )
    STATIC_ROOT= os.path.join(BASE_DIR, '../choirplanner_static/static')
    #MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_ROOT = os.path.join(STATIC_ROOT, '../media')
    
    tdir = [os.path.join(BASE_DIR, 'templates'),]
    DEBUG = True
    td = True
    print "STATIC_ROOT = " + STATIC_ROOT
    SITE_ID=2
    JAVA_GATEWAY_ADDRESS = '127.0.0.1'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                },
            'NAME': 'choirplanner',
            'USER': 'choirplanner',
            'PASSWORD': 'choirplanner',
            'HOST': '127.0.0.1',
            }
        }
    STATIC_URL = '/static/static/'
    MEDIA_URL = '/static/media/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
        )
    STATIC_ROOT= os.path.join(BASE_DIR, '../../praisingvoices_static/static')
    MEDIA_ROOT = os.path.join(BASE_DIR, '../../praisingvoices_static/media')
    #MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
    STATIC_ROOT = '/home/jchinte/webapps/praisingvoices_static/static'
    
    tdir = [os.path.join(BASE_DIR, 'templates'),]
    DEBUG = False
    td = True
    print "STATIC_ROOT = " + STATIC_ROOT
    SITE_ID=2
    JAVA_GATEWAY_ADDRESS = '127.0.0.1'

print "MEDIA_ROOT="+MEDIA_ROOT
print "STATIC_ROOT="+STATIC_ROOT

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
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': tdir,
        'OPTIONS': {
            'debug': td,
            'context_processors': [ 
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                'django.core.context_processors.request',
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

