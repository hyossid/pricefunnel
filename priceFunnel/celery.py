from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'priceFunnel.settings')

app = Celery('priceFunnel')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cron job scheduled 30 mins after NYSE closing time.
# Django App time set to HKT
app.conf.beat_schedule = {
    'get_EOD_data': {
        'task': 'MarketPrice.tasks.get_data',
        'schedule': crontab(hour=4, minute=30, day_of_week='2-6'),
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

