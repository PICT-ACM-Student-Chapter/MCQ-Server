"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_SDK_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default="django-insecure-ncs&&)001*$$7mgs822pvidtwj(pf=jc=g851__q!ysy5bkwzk",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DJANGO_DEBUG", default=True))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "corsheaders",
    "rest_framework",
    "core",
    "djoser",
    "martor",
    "csvexport",
    "drf_yasg",
    "django_celery_results",
    "silk",
    "import_export"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

AUTH_USER_MODEL='core.User'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Token",),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
}

# Rest Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

# CELERY SETTINGS
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

# DJOSER SETTINGS 
DJOSER = {
    'SERIALIZERS': {
        'current_user': 'core.serializers.CustomUserSerializer'
    },
}

# CSV EXPORT SETTINGS 
CSV_EXPORT_REFERENCE_DEPTH = 3
CSV_EXPORT_EMPTY_VALUE = ''

# MARTOR SETTINGS
MARTOR_THEME = 'semantic'
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',  # to enable/disable emoji icons.
    'imgur': 'true',  # to enable/disable imgur/custom uploader.
    'mention': 'false',  # to enable/disable mention
    'jquery': 'true',
    # to include/revoke jquery (require for admin default django)
    'living': 'false',  # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',  # to enable/disable hljs highlighting in preview
}

# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'horizontal', 'heading', 'pre-code',
    'blockquote', 'unordered-list', 'ordered-list',
    'link', 'image-link', 'image-upload', 'emoji',
    'direct-mention', 'toggle-maximize', 'help'
]

# To setup the martor editor with title label or not (default is False)
MARTOR_ENABLE_LABEL = False

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify'  # default
MARTOR_MARKDOWNIFY_URL = '/martor/markdownify/'  # default

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins',  # ~~strikethrough~~ and ++underscores++
    'martor.extensions.mention',  # to parse markdown mention
    'martor.extensions.emoji',  # to parse markdown emoji
    'martor.extensions.mdx_video',  # to parse embed/iframe video
    'martor.extensions.escape_html',  # to handle the XSS vulnerabilities
]

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = {}

# Markdown urls
MARTOR_UPLOAD_URL = '/martor/uploader/'  # default
MARTOR_SEARCH_USERS_URL = '/martor/search-user/'  # default

# Markdown Extensions
# MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://www.webfx.com/tools/emoji-cheat-sheet/graphics/emojis/'     # from webfx
MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://github.githubassets.com/images/icons/emoji/'  # default from github
MARTOR_MARKDOWN_BASE_MENTION_URL = 'https://python.web.id/author/'  # please change this to your domain
# CACHE SETTINGS
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://redis-cache:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "PASSWORD": "YourPasswordHere1234"
#         }
#     }
# }

# SILK SETTINGS 
SILKY_PYTHON_PROFILER = True
SILKY_AUTHENTICATION = True 
SILKY_AUTHORISATION = True  

# ADMIN PANEL SETTINGS
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "MCQ Server Admin Panel",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "MCQ Server",
    "site_header": "MCQ Server",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # "related_modal_active": True,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the MCQ Server Admin Panel",
    "show_ui_builder": True,
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-success",
    },
}