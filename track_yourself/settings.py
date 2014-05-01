"""
Django settings for track_yourself project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@6q1!ya(e)7bdst8)db9up8oc3r11%eqtp@dqk)@%^lvf$thgc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

SESSION_ENGINE =  'django.contrib.sessions.backends.file'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'track_yourself.urls'

WSGI_APPLICATION = 'track_yourself.wsgi.application'

#Used for serving static content (like displaying a pdf)
MEDIA_ROOT = '/users/kdrahbar/djcode/media'
MEDIA_URL = '/media/'
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "SE_DATABASE_SCHEMA",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
} """
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "mydb",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}"""


TEMPLATE_DIRS = (
   '/Users/Dorel/Dropbox/Spring2014/CSE360/PROJECT/git-trackyourself/trackyourself/templates',
    #'/users/kdrahbar/dev/trackyourself/templates',
   # '/users/kdrahbar/merucrial/track_yourself/templates',
)
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'


# Bootstrap stuff
STATICFILES_DIRS = (
    '/Users/Dorel/Dropbox/Spring2014/CSE360/PROJECT/git-trackyourself/trackyourself/static',
   #'/users/kdrahbar/dev/trackyourself/static',
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(
        os.path.dirname(__file__),
        'static',
    ),
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'trackyourselfCSE360@gmail.com'
EMAIL_HOST_PASSWORD = '19badpass93word'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'trackyourselfCSE360@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
