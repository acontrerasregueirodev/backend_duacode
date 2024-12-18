import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key (ensure to keep this safe in production)
SECRET_KEY = 'django-insecure-fg9l&4x*jdh+1ct_*g4$1r1q9i-gi)@gs998x8olw537p$az7o'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# SESSION_COOKIE_DOMAIN = "localhost"
# CSRF and CORS settings
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000','http://localhost:8000','https://localhost:3000','https://localhost:8000']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # tu frontend React
    'http://127.0.0.1:8000',  # tu backend Django
    'https://localhost:3000',  # si tienes un entorno seguro en local
    'https://localhost:8000',  # si tienes un entorno seguro en local
]
CORS_ALLOW_CREDENTIALS = True  # Permitir que las cookies y credenciales se envíen
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Asegúrate de que esté configurado correctamente

# Si es necesario, también puedes agregar:
# CORS_ALLOW_HEADERS = [
#     'content-type',
#     'x-csrftoken',
# ]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'corsheaders',
    'proyectos',
    'subir_archivo',
    'sedes',
    'mapa',
    'contacto',
    'codigo_qr',
    'login',
    'dashboard',   
]

LOGOUT_REDIRECT_URL = '/'


# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Should be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL configurations
ROOT_URLCONF = 'proyecto_duacode.urls'

# Templates settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['dashboard/templates',],
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
# Asegúrate de que el token se lea desde las cookies
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_COOKIE': 'access_token',  # Cookie con el token de acceso
    'USER_ID_FIELD': 'username',
    'USER_ID_CLAIM': 'username',
}
WSGI_APPLICATION = 'proyecto_duacode.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Carpeta donde se guardarán los archivos estáticos


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


