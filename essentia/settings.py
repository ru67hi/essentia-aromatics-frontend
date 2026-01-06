from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

# --------------------
# APPLICATIONS
# --------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store',
    'cloudinary',
    'cloudinary_storage',
]

# --------------------
# MIDDLEWARE
# --------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# --------------------
# URLS & TEMPLATES
# --------------------
ROOT_URLCONF = 'essentia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # ✅ Correct template directory
        'DIRS': [BASE_DIR / 'store' / 'templates'],

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

# --------------------
# DATABASE
# --------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------
# STATIC FILES (CSS, JS, IMAGES)
# --------------------
STATIC_URL = '/static/'

# ✅ THIS IS CORRECT FOR YOUR PROJECT
STATICFILES_DIRS = [
    BASE_DIR / 'store' / 'static',
]

# --------------------
# MEDIA FILES (Product Images)
# --------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------
# AUTH
# --------------------
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

# --------------------
# EMAIL (DEV)
# --------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'essentiaromatics16@gmail.com'
EMAIL_HOST_PASSWORD = 'csewfrwprazbkdfs'

DEFAULT_FROM_EMAIL = "essentiaromatics16@gmail.com"



# --------------------
# REQUIRED (Django 4+)
# --------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ALLOWED_HOSTS = ['*']

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE= 'whitenoise.storage.compressedManifestStaticFilesStorage'

CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

DEBUG = False


ALLOWED_HOSTS = ["*" , ".onrender.com"]


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'deyw1xlsa',
    'API_KEY': '528778421333263',
    'API_SECRET': 't1pJPh7IF0qlhHEantap1H521OU',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
