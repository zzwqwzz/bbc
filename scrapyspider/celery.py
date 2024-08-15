from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

cel = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/1', include=[
    'scrapyspider.run',
    'scrapyspider.auto_trans'
])
cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False

cel.conf.beat_schedule = {
    'spider-add-everyday': {
        'task': 'scrapyspider.run.spider',
        'schedule': crontab(minute="*/10", hour="0"),
        'args': ()
    },
    'trans-add-everyday': {
        'task': 'scrapyspider.auto_trans.auto_trans',
         'schedule': crontab(minute="10", hour="1"),
        'args': ()
    }
}