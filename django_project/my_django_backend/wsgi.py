"""
WSGI config for my_django_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Fetching API data required libraries
import threading
from schedule import every, repeat, run_pending
import time
import pysftp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_backend.settings')

application = get_wsgi_application()

# Mechanism to run background processes
def run_continuously(interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

@repeat(every(20).seconds)
def get_weather_report():
    with pysftp.Connection(str(os.environ['REMOTE_IP']), username=str(os.environ['REMOTE_USERNAME']), password=str(os.environ['REMOTE_PASSWORD'])) as sftp:
        with sftp.cd('fetched_data'):
            sftp.get('current_weather.txt', preserve_mtime=True)

# Check every <INTERVAL> for pending scheduled tasks
stop_run_continuously = run_continuously()

# KILLSWITCH IN CASE NEEDED
# stop_run_continuously.set()