INSTALLED_APPS = [
    # ...
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ip_tracking",
    "ratelimit",
]

MIDDLEWARE = [
    # ...
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "ip_tracking.middleware.IPTrackingMiddleware",
]

# Celery config (basic)
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
