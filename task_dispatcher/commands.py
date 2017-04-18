# -*- coding: utf-8 -*-
import os

from celery.bin.beat import beat as beat_bin
from celery.bin.worker import worker as worker_bin

from clinner.command import command
from clinner.exceptions import ImproperlyConfigured
from clinner.run import Main
from task_dispatcher.celery import app
from task_dispatcher.register import register
from task_dispatcher.settings import settings

_worker_bin = worker_bin(app=app)
_beat_bin = beat_bin(app=app)

SHOW_JSON = 'json'
SHOW_YAML = 'yaml'
SHOW_CHOICES = (SHOW_JSON, SHOW_YAML)


@command(args=_worker_bin.add_arguments, parser_opts={'help': 'Run a consumer.'})
def consumer(*args, **kwargs):
    """
    Run a consumer process.
    """
    kwargs['queues'] = kwargs['queues'] or ['consumer']
    kwargs['hostname'] = kwargs['hostname'] or 'consumer@%h'
    worker = app.Worker(**kwargs)
    worker.start()
    return worker.exitcode


@command(args=_worker_bin.add_arguments, parser_opts={'help': 'Run a producer.'})
def producer(*args, **kwargs):
    """
    Run a producer process.
    """
    kwargs['queues'] = kwargs['queues'] or ['producer']
    kwargs['hostname'] = kwargs['hostname'] or 'producer@%h'
    worker = app.Worker(**kwargs)
    worker.start()
    return worker.exitcode


@command(args=_beat_bin.add_arguments, parser_opts={'help': 'Run the scheduler.'})
def scheduler(*args, **kwargs):
    """
    Run a scheduler process.
    """
    beat = app.Beat(**kwargs)

    for task, task_args, task_kwargs in settings.run_at_startup:
        app.send_task(task, args=task_args, kwargs=task_kwargs)

    return beat.run()


@command(args=((('-f', '--format'), {'choices': SHOW_CHOICES, 'default': SHOW_YAML}),),
         parser_opts={'help': 'Lists all producers and consumers registered.'})
def show(*args, **kwargs):
    """
    Lists all producers and consumers registered.
    """
    if kwargs['format'] == SHOW_YAML:
        print(register.to_yaml())
    else:
        print(register.to_json())


class TaskDispatcherCommand(Main):
    """
    Command for running producer, consumer and scheduler processes along with some other utilities. This acts as a
    Command Line Interface for Task dispatcher.
    """
    description = 'Task dispatcher command that provides a common entry point for running the different processes as ' \
                  'well as some utilities.'

    def inject_app_settings(self):
        if self.settings:
            os.environ['TASK_DISPATCHER_SETTINGS'] = self.settings

        if 'TASK_DISPATCHER_SETTINGS' not in os.environ:
            raise ImproperlyConfigured('Settings not defined')
