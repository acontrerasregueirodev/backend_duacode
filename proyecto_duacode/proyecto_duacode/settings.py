import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key (ensure to keep this safe in production)
SECRET_KEY = 'django-insecure-fg9l&4x*jdh+1ct_*g4$1r1q9i-gi)@gs998x8olw537p$az7o'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SESSION_COOKIE_DOMAIN = "localhost"
# CSRF and CORS settings
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000','http://localhost:8000','https://localhost:3000','https://localhost:8000']
CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://localhost:8000']
CORS_ALLOW_CREDENTIALS = True  # Permitir que las cookies y credenciales se envíen
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Asegúrate de que esté configurado correctamente

# Si es necesario, también puedes agregar:
# CORS_ALLOW_HEADERS = [
#     'X-CSRFToken',  # Asegúrate de permitir el encabezado CSRFToken
#     'Authorization',  # Si usas autorización con JWT o SessionID
# ]
CORS_ALLOW_ALL_ORIGINS = True



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
]

#CSRF_COOKIE_SECURE = False  
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

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',  # Para autenticación por token
        'rest_framework.authentication.SessionAuthentication',  # Para autenticación por sesión
    ],
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

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Uncomment the email configuration if needed
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.pythonanywhere.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'belami@pythonanywhere.com'
# EMAIL_HOST_PASSWORD = 'Figura00+'
# DEFAULT_FROM_EMAIL = 'contacto@pythonanywhere.com'
