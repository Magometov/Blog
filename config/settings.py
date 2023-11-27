import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

# ======================================================================================================================
# BASE SETTINGS
# ======================================================================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

# ======================================================================================================================
# BASE APPS
# ======================================================================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ======================================================================================================================
# OTHER PACKAGES
# ======================================================================================================================

INSTALLED_APPS += [
    "rest_framework",
    "corsheaders",
    "debug_toolbar",
    'djoser',
]

# ======================================================================================================================
# MY APPS
# ======================================================================================================================

INSTALLED_APPS += [
    "apps.core.apps.CoreConfig",
    "apps.api.apps.ApiConfig",
    'apps.api_v1.apps.ApiV1Config',
]

# ======================================================================================================================
# SPECTACULAR
# ======================================================================================================================

INSTALLED_APPS += [
    "drf_spectacular",
]

# ======================================================================================================================
# MIDDLEWARE SETTINGS
# ======================================================================================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================================================================================================================
# ROOT URL SETTINGS
# ======================================================================================================================

ROOT_URLCONF = 'config.urls'

# ======================================================================================================================
# TEMPLATES SETTINGS
# ======================================================================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# ======================================================================================================================
# WSGI SETTINGS
# ======================================================================================================================

WSGI_APPLICATION = 'config.wsgi.application'

# ======================================================================================================================
# DATABASE SETTINGS
# ======================================================================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PG_DATABASE'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# ======================================================================================================================
# DJANGO REST FRAMEWORK SETTINGS
# ======================================================================================================================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"
}

# ======================================================================================================================
# SPECTACULAR SETTINGS
# ======================================================================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Test",
    "DESCRIPTION": "Test",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
}

# ======================================================================================================================
# DJOSER SETTINGS
# ======================================================================================================================

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {},
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
}

# ======================================================================================================================
# MORE SETTINGS
# ======================================================================================================================

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


AUTH_USER_MODEL = "core.User"

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ======================================================================================================================
# STATIC AND MEDIA SETTINGS
# ======================================================================================================================

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "/static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "/media/")

# ======================================================================================================================
# CORS SETTINGS
# ======================================================================================================================

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CSRF_COOKIE_SECURE = False


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
