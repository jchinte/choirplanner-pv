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


SECRET_KEY = '%eer7)u5#$v&xdlgwxjd12nq$g#y@%q9odd))#+%n-xetb)-ym'
DEBUG = False

if DEBUG:
    #ALLOWED_HOSTS=['http://localhost:3000']
    # CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = (
        'http://localhost:8000',
        'http://localhost:3000',
        'http://127.0.0.1:8000',
        'http://127.0.0.1:3000',
        'http://192.168.1.245:3000',
        'https://praisingvoices.org',
        'http://108.65.170.64:8000',
    )
CSRF_TRUSTED_ORIGINS = ["https://praisingvoices.org", "https://www.praisingvoices.org"]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
#SESSION_COOKIE_SECURE=False
#SESSION_COOKIE_DOMAIN='127.0.0.1'
ALLOWED_HOSTS = ['*']


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        #'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django_registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SongManager',
    'Event_Planner.apps.Event_PlannerConfig',
    'dh5bp',
    'dh5mbp',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_crontab',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    'dj_rest_auth',
    'pv_blog',
    'wagtail.contrib.routable_page',
    'menus',
    'django_extensions',
    'protected_media',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    #'ssl_redirect.middleware.SSLRedirectMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

WAGTAIL_SITE_NAME = 'pv'

ROOT_URLCONF = 'music_planner0.urls'

WSGI_APPLICATION = 'music_planner0.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'praisingvoices_postgres',
        'USER': 'pvdb',
        'PASSWORD': 'PuT9{pB}3$pxX2[B',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },

}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'templates', 'dist', '_assets'),
    os.path.join(BASE_DIR, 'templates', 'dist', 'css'),
    )
STATIC_ROOT= os.path.join(BASE_DIR, '../../praisingvoices_static/static')
MEDIA_ROOT = os.path.join(BASE_DIR, '../../praisingvoices_static/media')
PROTECTED_MEDIA_ROOT = "%s/protected/" % BASE_DIR
PROTECTED_MEDIA_URL = "/protected"
PROTECTED_MEDIA_SERVER = "nginx"  # Defaults to "django"
PROTECTED_MEDIA_LOCATION_PREFIX = "/internal"  # Prefix used in nginx config
PROTECTED_MEDIA_AS_DOWNLOADS = False  # Controls inclusion of a Content-Disposition header
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = (
#     '/home/jchinte/home/webapps/praisingvoices2/choirplanner_pv/static/',
#     )
SITE_ID=2
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SERIALIZATION_MODULES = {
                         'json': 'wadofstuff.django.serializers.json2' 
                         }
LOGIN_REDIRECT_URL='/events/'
LOGIN_URL='/accounts/login'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'OPTIONS': {
            'debug': True,
            'context_processors': [ 
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",                             
                'context_processors.dh5mbp_jquery_mobile',
                'django.template.context_processors.request',
                'wagtail.contrib.settings.context_processors.settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',           
            ]
        },
    },
]

EMAIL_HOST='mail.praisingvoices.org'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='praisingvoices@praisingvoices.org'
EMAIL_HOST_PASSWORD='%AJ$+q4-+f$b`"hy'
DEFAULT_FROM_EMAIL='praisingvoices@praisingvoices.org'
SERVER_EMAIL='praisingvoices@praisingvoices.org'
ACCOUNT_ACTIVATION_DAYS=7
REGISTRATION_OPEN=False
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_ADMINS=[('jchinte','jchinte@gmail.com'),]
REGISTRATION_FORM='registration_pv.forms.PVRegistrationForm'
ADMINS=[('jchinte','jchinte@gmail.com'),]
FILE_UPLOAD_PERMISSIONS=0o644
TEMPLATE_CONTEXT_PROCESSORS = (
     'django.template.context_processors.request',
)

CRONJOBS = [
    ('0 0 * * 0', 'SongManager.cron.cleanComposers')
]