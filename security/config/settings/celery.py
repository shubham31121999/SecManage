from config.env import env


CELERY_BROKER_URL = env("CELERY_BROKER_URL")