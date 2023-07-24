import os
from celery import Celery
from celery.signals import task_prerun, task_postrun

from config.redis import r

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('Factory')
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_direct_queue(sender, **kwargs):
    sender.conf.task_routes = {"*": {"queue": "celery"}}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@task_prerun.connect
def task_prerun(task_id, task, *args, **kwargs):
    r.lpush('tasks', task_id)


@task_postrun.connect
def task_postrun(task_id, task, *args, **kwargs):
    r.lrem('tasks', 1, task_id)

app.autodiscover_tasks()
