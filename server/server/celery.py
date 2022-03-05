import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': '',
#         'schedule': 10.0,
#     },
# }
# app.conf.timezone = 'UTC'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request:', self.request)
