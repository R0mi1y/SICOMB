import json
from pathlib import Path
import os
import socket

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-=@-^(fuzcew496ttksj^_=+irgt1xd5oc86f2wr0ck6yo%qhtw"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Meus Apps 
    "police",
    "equipment",
    "load",
    "report",
    
    # Apps de terceiros
    "corsheaders",  # Configuração necessaria para acerro da página equipment/get como uma api
]
    
MIDDLEWARE = [
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "SICOMB.middlwares.handle_error",
]

APPEND_SLASH = True  # resolve erro do fetch de rotas do django

ROOT_URLCONF = "SICOMB.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'SICOMB.context_processors.global_variables',
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "SICOMB.wsgi.application"

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

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

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
        "PASSWORD": "root",
        # "PASSWORD": "12345679",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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


CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
]

CORS_ALLOW_HEADERS = [
    "cache-control",
    "Content-Type"
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
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        # 'handlers': ['console'],
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO', 
    },
}

# Variável auxiliar do sistema

AUX = {
    "matricula": "",
    "uids": [],
    "registering_fingerprint": {
        'police_id': None,
        'status': False,
        'fingetprint_id': None,
    },
    
    "confirm_cargo": False,
    "list_equipment": [],
    "list_equipment_valid": False,
    "key_token_login_police": None,
    
    "messsage_serial_port": None,
    "is_requesting_load": False,
    
    # ======================= SENSORES =========================
    "serial_port_rfid": None,
    "serial_port_fingerprint": None,
    
    # LEITOR DE DIGITAL
    "message_fingerprint_sensor": None,
    "PORT_RFID": "COM13",
}


def get_local_ip():
    try:
        # Cria um socket UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Conecta-se a um servidor externo (não há tráfego real)
        s.connect(('8.8.8.8', 80))
        
        # Obtém o endereço IP local
        local_ip = s.getsockname()[0]
        
        return local_ip
    except socket.error:
        return None
    finally:
        # Fecha o socket
        s.close()
    

def ler_settings():
    caminho_arquivo = os.path.join(STATICFILES_DIRS[0], 'json', 'settings.json')
    
    sett = None
    
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            sett = json.load(arquivo)

        sett['ip'] = get_local_ip()
    except FileNotFoundError:
        print("Arquivo não encontrado")

    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")
        
    
    return sett

AUX = {**AUX, **ler_settings()}