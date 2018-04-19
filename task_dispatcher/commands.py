# -*- coding: utf-8 -*-
import itertools
import logging
import os
from _socket import gethostname
from importlib import import_module

from celery import Celery
from celery.bin.beat import beat as beat_bin
from celery.bin.worker import worker as worker_bin
from clinner.command import command
from clinner.exceptions import ImproperlyConfigured
from clinner.run import Main
from flower.command import FlowerCommand

from task_dispatcher.celery import app
from task_dispatcher.register import register
from task_dispatcher.settings import settings

logger = logging.getLogger(__name__)

_worker_bin = worker_bin(app=Celery())
_beat_bin = beat_bin(app=Celery())

SHOW_JSON = 'json'
SHOW_YAML = 'yaml'
SHOW_CHOICES = (SHOW_JSON, SHOW_YAML)


@command(args=_worker_bin.add_arguments, parser_opts={'help': 'Run a consumer.'})
def consumer(*args, **kwargs):
    """
    Run a consumer process.
    """
    kwargs['queues'] = kwargs.get('queues') or ['consumer']
    kwargs['hostname'] = kwargs.get('hostname') or 'consumer@{}'.format(gethostname())
    worker = app.Worker(**kwargs)
    worker.start()
    return worker.exitcode


@command(args=_worker_bin.add_arguments, parser_opts={'help': 'Run a producer.'})
def producer(*args, **kwargs):
    """
    Run a producer process.
    """
    kwargs['queues'] = kwargs.get('queues') or ['producer']
    kwargs['hostname'] = kwargs.get('hostname') or 'producer@{}'.format(gethostname())
    worker = app.Worker(**kwargs)
    worker.start()
    return worker.exitcode


@command(args=_beat_bin.add_arguments, parser_opts={'help': 'Run the scheduler.'})
def scheduler(*args, **kwargs):
    """
    Run a scheduler process.
    """
    beat = app.Beat(**kwargs)

    # Remove old startup tasks
    startup_tasks = [t[0] for t in settings.run_at_startup]
    inspect = app.control.inspect()
    tasks = itertools.chain(
        (t for worker_tasks in (inspect.scheduled().values() if inspect.scheduled() else []) for t in worker_tasks),
        (t for worker_tasks in (inspect.active().values() if inspect.active() else []) for t in worker_tasks),
        (t for worker_tasks in (inspect.reserved().values() if inspect.reserved() else []) for t in worker_tasks),
    )
    tasks = {(t['id'], t['name']) for t in tasks}
    app.control.revoke([id_ for id_, name in tasks if name in startup_tasks])

    # Load startup tasks
    for task_path, task_args, task_kwargs in settings.run_at_startup:
        try:
            task_module, task_name = task_path.rsplit('.', 1)
            task = getattr(import_module(task_module), task_name)
        except:
            logger.error('Cannot load task "%s"', task_path)
        else:
            task.delay(*task_args, **task_kwargs)

    return beat.run()


@command(args=((('-f', '--format'), {'choices': SHOW_CHOICES, 'default': SHOW_YAML}),),
         parser_opts={'help': 'Lists all producers and consumers registered.'})
def show(*args, **kwargs):
    """
    Lists all producers and consumers registered.
    """
    if kwargs.get('format') == SHOW_YAML:
        print(register.to_yaml())
    else:
        print(register.to_json())


@command(parser_opts={'help': 'Run Flower monitoring tool.'})
def flower(*args, **kwargs):
    """
    Run Flower monitoring tool.
    """
    args = ('flower',) + args
    flower_cmd = FlowerCommand(app=app)
    flower_cmd.execute_from_commandline(argv=args)


class TaskDispatcherCommand(Main):
    """
    Command for running producer, consumer and scheduler processes along with some other utilities. This acts as a
    Command Line Interface for Task dispatcher.
    """
    description = 'Task dispatcher command that provides a common entry point for running the different processes as ' \
                  'well as some utilities.'

    def inject_app_settings(self):
        if self.args.settings:
            os.environ['TASK_DISPATCHER_SETTINGS'] = self.args.settings

        if 'TASK_DISPATCHER_SETTINGS' not in os.environ:
            raise ImproperlyConfigured('Settings not defined')
