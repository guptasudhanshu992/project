from pathlib import Path
import os
#from dotenv import load_dotenv
import environ
#import timedelta

#load_dotenv()

env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%^+fffx19eo^4z41#lq*ykz%7lplkqs5ux_6$8e!ci%8@t@=uk"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

MACHINE = env('MACHINE')

AWS_ACCESS_KEY_ID=env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME=env('AWS_S3_REGION_NAME')
AWS_QUERYSTRING_EXPIRE=int(env('AWS_QUERYSTRING_EXPIRE'))

AWS_S3_CUSTOM_DOMAIN=env('AWS_S3_CUSTOM_DOMAIN')

AWS_CLOUDFRONT_KEY_ID=env('AWS_CLOUDFRONT_KEY_ID')
#AWS_CLOUDFRONT_KEY=env('AWS_CLOUDFRONT_KEY')
AWS_CLOUDFRONT_KEY_PATH = os.path.join(BASE_DIR, 'private_key.pem')

try:
    with open(AWS_CLOUDFRONT_KEY_PATH, 'r') as key_file:
        AWS_CLOUDFRONT_KEY = key_file.read()
except FileNotFoundError:
    raise Exception(f"Private key file not found at {AWS_CLOUDFRONT_KEY_PATH}. Please check the file path.")
except Exception as e:
    raise Exception(f"Error reading private key file: {e}")

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "core",
    "blog",
    "accounts",
    "courses",
    "ckeditor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if MACHINE == 'LOCAL':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [BASE_DIR / 'static/']
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media/'

else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.mysql"),
            "NAME": os.getenv("DB_NAME", default=""),
            "USER": os.getenv("DB_USER", default=""),
            "PASSWORD": os.getenv("DB_PASSWORD", default=""),
            "HOST": os.getenv("DB_HOST", default=""),
            "PORT": os.getenv("DB_PORT", default=""),
            "OPTIONS": {
                "sql_mode": "STRICT_TRANS_TABLES",
            },
        }
    }

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIAFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

#STATIC_ROOT = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
#STATICFILES_DIRS = [
#    BASE_DIR / 'static/',
#]
#MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'accounts.Users'

# CKEditor configurations
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # Use 'basic' or customize the toolbar as needed
        'height': 300,
        'width': 'auto',
    },
}