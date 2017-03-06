"""
Django settings for silo project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # The root of the front end + backend
print("Set BASE_DIR={}".format(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lb6a$b2(%3a*ddryv68b1ijq1sa(uctc)99yt2wq@u7!&q_f_c'

APP_ENV = os.environ.get('APP_ENV') or 'development'
PRODUCTION = APP_ENV == 'production'
DEVPRODUCTION = APP_ENV == 'devproduction'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TWILIO_STATUS_CALLBACK = 'http://silo.ngrok.io/api/status/messages/'

ALLOWED_HOSTS = ['.ngrok.io', 'localhost', '.elasticbeanstalk.com']
CORS_ORIGIN_WHITELIST = (
    'silo.ngrok.io',
    'localhost:3000',
    'silo-web-dev-test.us-west-1.elasticbeanstalk.com',
    'dashboard.silohq.com',
    'devdashboard.silohq.com',
)
CORS_ALLOW_CREDENTIALS = True

# Django Channels settings for Development
###############################################
# Use Different Settings for Production!!!!   #
###############################################
CHANNEL_LAYERS = {
    "default": {
    "BACKEND": "asgiref.inmemory.ChannelLayer",
    "ROUTING": "silo.routing.channel_routing",
    },
}

# Dev production or production environment setup
if PRODUCTION or DEVPRODUCTION:
    print('~~~~~~~~~~~~~~~~~~~~~~~~' + APP_ENV + '~~~~~~~~~~~~~~~~~~~~~~~~')
    ALLOWED_HOSTS += ['.silohq.com']
    TWILIO_STATUS_CALLBACK = 'https://www.silohq.com/api/status/messages/'

    # Django Channels settings for Production
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "ROUTING": "silo.routing.channel_routing",
        },
    }


if PRODUCTION:
    DEBUG = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cors
    'corsheaders',

    # Channels
    'channels',

    # Webpack loader
    'webpack_loader',

    # Django extensions for shell_plus
    'django_extensions',

    # Django-rest-framework
    'rest_framework',
    'rest_framework.authtoken',

    # Django-rest-auth
    'rest_auth',
    'django.contrib.sites',
    'rest_auth.registration',

    # Django-All-Auth
    'allauth.socialaccount',
    'allauth',
    'allauth.account',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',

    # Silo apps
    'messagesapp',
    'contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'silo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

##### djangorestframework
INCLUDE_SESSION_AUTHENTICATION = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGE_SIZE': 100
}

WSGI_APPLICATION = 'silo.wsgi.application'

# Django AllAuth Setup
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_SIGNUP_FORM_CLASS = 'contacts.forms.SignupForm'
ACCOUNT_EMAIL_VERIFICATION = False

# TODO: get a proper email backend so we can send authentication emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DB_NAME = os.environ['RDS_DB_NAME'] if 'RDS_DB_NAME' in os.environ else 'silo2'
DB_USER = os.environ['RDS_USERNAME'] if 'RDS_USERNAME' in os.environ else 'silomanager'
DB_PASS = os.environ['RDS_PASSWORD'] if 'RDS_PASSWORD' in os.environ else 'silomanagerpassword'
DB_HOST = os.environ['RDS_HOSTNAME'] if 'RDS_HOSTNAME' in os.environ else 'localhost'
DB_PORT = os.environ.get('RDS_PORT') if 'RDS_PORT' in os.environ else 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = (
#     # os.path.join(BASE_DIR, 'assets'), # We do this so that django's collectstatic copies or our bundles to the STATIC_ROOT or syncs them to whatever storage we use.
#     os.path.join(PROJECT_ROOT, 'silo-web/client/assets'),
# )

# Webpack loader
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

# Site ID
SITE_ID = 1
