from .settings import *
import os
import environ


# Initialize environment variables
env = environ.Env()
environ.Env.read_env()


DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://trusted-scripts.com")
CSP_STYLE_SRC = ("'self'", "https://trusted-styles.com")

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://subdomain.example.com",
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]

CORS_ALLOW_CREDENTIALS = True
RATELIMIT_GLOBAL = '100/h'  # Limits all requests to 100 per hour


# Database settings (PostgreSQL, for example)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Mailchimp Configuration
MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = env('MAILCHIMP_DATA_CENTER')  # The data center is part of your API key (e.g., 'usX')
MAILCHIMP_AUDIENCE_ID = env('MAILCHIMP_AUDIENCE_ID')

# Email Backend Configuration (SendGrid or SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'  # Replace with SendGrid or other email service
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('SENDGRID_USERNAME')  # Your SendGrid username
EMAIL_HOST_PASSWORD = env('SENDGRID_PASSWORD')  # Your SendGrid API key or password
DEFAULT_FROM_EMAIL = 'your_email@example.com'


# Static and media file settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = "blog.CustomUser"

