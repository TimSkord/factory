## **Redis**

Run docker container

```shell
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

Install library
```shell
pip install redis
```
---
## **PG**

Run docker container

```shell
sudo docker run --name factory-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
```

Install library

```shell
pip install psycopg2-binary
```

*settings.py*

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run migrations

```shell
python manage.py migrate
```
---

## **Celery**

Install library

```shell
pip install celery
pip install celery-progress
```

*settings.py*

```python
INSTALLED_APPS = (
    # ...
    'celery_progress',
    # ...
)

# ...
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_ALWAYS_EAGER = False
# ...
```

Run Celery

```shell
celery -A config worker --loglevel=info
```

* **config** - path to the folder where the **celery.py** file is located

Kill all workers processes

```shell
pkill -f 'celery worker
```
---