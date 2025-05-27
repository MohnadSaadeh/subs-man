# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import sys
from decouple import config
from unipath import Path
from datetime import timedelta
# from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = Path(__file__).parent




CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# sys.path.append(os.path.join(BASE_DIR, 'apps')) #neeeeeewwwwwwwwwwww

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
#DEBUG = False

# load production server from .env
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]
# ALLOWED_HOSTS = ['192.168.1.133', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    'daphne', # you have to put it first ######## Daphne package, which is required for running an ASGI server.
    'django_tenants',  # مكتبة إدارة المستأجرين
    # 'tenants',  # التطبيق الذي سينظم المستأجرين
    'landing',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'apps.home', # التطبيق الأساسي الخاص بك
    'channels',
    # 'apps.home' , # Enable the inner home (home)
    'apps.home.apps.HomeConfig',  # Use the full path to your AppConfig (signals)
    #for crispy pip install crispy-bootstrap5
    #for crispy 
    'whitenoise',
    'crispy_forms',    
    'crispy_bootstrap5',
    # 'axes',
]
#for crispy
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"


# يجب إضافة هذا السطر ليعرف Django أي نموذج هو المستأجر:
TENANT_MODEL = "tenants.Client"
TENANT_DOMAIN_MODEL = 'tenants.Domain'  # أو النموذج الذي تستخدمه لإدارة الدومين
PUBLIC_SCHEMA_NAME = "public"

# التطبيقات المشتركة بين جميع المستأجرين (يمكن أن تكون تطبيقات مثل إدارة المستأجرين)
SHARED_APPS = [
    'django_tenants',  # تطبيق django-tenants نفسه
    'tenants.apps.TenantsConfig',  # التطبيق الذي يدير المستأجرين
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # for crispy important to put it here 
    'whitenoise',
    'crispy_forms',
    'crispy_bootstrap5',
    # 'axes',
]


# التطبيقات التي سيتم تحميلها لكل مستأجر
# هي التطبيقات التي تخص كل مستأجر
TENANT_APPS = [
    
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise',
    'apps.home',  # تطبيقك الخاص
    # 'landing',
    # إضافة أي تطبيقات أخرى يحتاج المستأجر إليها
    'axes',


]
INSTALLED_APPS = list(dict.fromkeys(SHARED_APPS + TENANT_APPS))



# MIDDLEWARE = [
#     'django_tenants.middleware.main.TenantMainMiddleware',  # Middleware for multi-tenant support
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.middleware.locale.LocaleMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'axes.middleware.AxesMiddleware',
# ]
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # يجب أن يكون أول Middleware للتأكد من تحديد المخطط (schema)

    # Security and static files
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # لتقديم الملفات الثابتة في الإنتاج

    # Session and authentication
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # يجب أن يأتي بعد SessionMiddleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Localization
    'django.middleware.locale.LocaleMiddleware',

    # Security extras
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third-party middleware
    'axes.middleware.AxesMiddleware',  # يفضل وضعه بعد AuthenticationMiddleware
]
#STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]
AXES_FAILURE_LIMIT = 3  # number of allowed attempts
# AXES_COOLOFF_TIME = 1  # in hours
AXES_COOLOFF_TIME = timedelta(minutes=1)
AXES_LOCKOUT_TEMPLATE = 'registration/account_locked.html'  # optional




ROOT_URLCONF = 'core.urls'
# Decoration Route defined in home/urls.py
LOGIN_REDIRECT_URL = "/dashboard"  
LOGOUT_REDIRECT_URL = "/login" 

TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',  # هذا مهم جداً
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = "core.asgi.application" #WebSockets



CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # For development
    }
}



DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django_tenants.postgresql_backend',  # استخدم محرك django-tenants

        'NAME': 'clupdb',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
DATABASE_ROUTERS = [
    'django_tenants.routers.TenantSyncRouter'
]








# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
    ('he', 'עִברִית'),
]

# TIME_ZONE = 'UTC'
# تفعيل الترجمة الدولية
USE_I18N = True
USE_L10N = True

# USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################





###########################Translation##################################
# مساؤ الترجمات 
# LOCALE_PATHS = [
#     BASE_DIR / 'locale',
# ]
LOCALE_PATHS = [
    os.path.join(CORE_DIR, 'locale'),
]
###########################Translation##################################

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'