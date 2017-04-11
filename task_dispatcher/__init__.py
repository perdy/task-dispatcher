# -*- coding: utf-8 -*-
from task_dispatcher.celery import app
from task_dispatcher.decorators import producer, consumer
from task_dispatcher.register import register

__version__ = '1.2.2'
__license__ = 'GPLv3'

__author__ = 'José Antonio Perdiguero López'
__email__ = 'perdy.hh@gmail.com'

__url__ = 'https://github.com/PeRDy/task-dispatcher'
__description__ = 'Library that provides a system to generate tasks producers and consumers with ease.'

__all__ = ['producer', 'consumer', 'register', 'app']

default_app_config = 'task_dispatcher.apps.TaskDispatcher'
