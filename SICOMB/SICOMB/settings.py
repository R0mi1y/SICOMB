from pathlib import Path
import os
import serial

# Configure as configurações de CORS

# Adicione o middleware de CORS ao MIDDLEWARE do Django
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-=@-^(fuzcew496ttksj^_=+irgt1xd5oc86f2wr0ck6yo%qhtw"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "corsheaders",  # Configuração necessaria para acerro da página equipment/get como uma api
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "police",
    "equipment",
    "load",
    "django.contrib.contenttypes",
]
    
CORS_ORIGIN_ALLOW_ALL = True  # CORS configuração

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'SICOMB.middlwares.handle_error',
]

APPEND_SLASH = False  # resolve erro do fetch de rotas do django

ROOT_URLCONF = "SICOMB.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "SICOMB.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Bahia"

USE_I18N = True

USE_TZ = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # O nome do arquivo SQLite
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "sicomb",
        "USER": "root",
        "OPTIONS": {
            "sql_mode": "traditional",
        },
        "PASSWORD": "",
        # "PASSWORD": "12345679",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUX = {"UID": ""}

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
AUTH_USER_MODEL = "police.Police"
CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = [
    "police.auth_backends.MatriculaBackend",
    "police.auth_backends.NameBackend",
    "django.contrib.auth.backends.ModelBackend",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
]

CORS_ALLOW_HEADERS = [
    "cache-control",
    'Content-Type'
]

# Configurações de emails

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "edielromily01@gmail.com"
EMAIL_HOST_PASSWORD = "pvgybzhcgmltvbhh"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = 'edielromily01@gmail.com'
EMAIL_SENDER_NAME = 'SISCOEM'


ADMINS = [('Ediel Romily', 'edielromily7@gmail.com')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Variável auxiliar do sistema

AUX = {
    "matricula": "",
    "uids": [],
    "calibres": (
        ("", "SELECIONE"),
        ("9mm", "9mm"),
        (".45 ACP", ".45 ACP"),
        (".380 ACP", ".380 ACP"),
        (".40 S&W", ".40 S&W"),
        (".357 Magnum", ".357 Magnum"),
        (".44 Magnum", ".44 Magnum"),
        ("5.56mm", "5.56mm"),
        ("7.62mm", "7.62mm"),
        (".22 LR", ".22 LR"),
    ),
    "confirmCargo": False,
    "errors": [],
    "list_equipment": [],
    "list_equipment_valid": False,
    # "porta_serial": serial.Serial('COM13', 115200),
    "porta_serial": None,
    "token_login_police": None,
}

