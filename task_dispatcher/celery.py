# -*- coding: utf-8 -*-
from celery import Celery


app = Celery('task_dispatcher')
app.config_from_envvar('TASK_DISPATCHER_SETTINGS', silent=True)
