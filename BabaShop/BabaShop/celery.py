from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BabaShop.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')


app = Celery('BabaShop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
