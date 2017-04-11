# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from typing import Dict, Any

from celery.bin.beat import beat as beat_bin
from celery.bin.worker import worker as worker_bin

from task_dispatcher.celery import app
from task_dispatcher.register import register


class TaskDispatcherCommand:
    """
    Command for running producer, consumer and scheduler processes along with some other utilities. This acts as a
    Command Line Interface for Task dispatcher.
    """

    LIST_JSON = 'json'
    LIST_YAML = 'yaml'
    LIST_CHOICES = (LIST_JSON, LIST_YAML)
    description = 'Task dispatcher command that provides a common entry point for running the different processes as ' \
                  'well as some utilities.'

    def __init__(self, parse_args=True):
        """
        Command for running producer, consumer and scheduler processes along with some other utilities.

        :param parse_args: If true, parse sys args.
        """
        self.args = self.parse_arguments() if parse_args else {}

    def parse_arguments(self) -> Dict[str, Any]:
        """
        Parse sys args and transform it into a dict.

        :return: Arguments parsed in dict form.
        """
        parser = ArgumentParser(description=self.description)
        self.add_arguments(parser)
        return {k: v for k, v in vars(parser.parse_args()).items()}

    def add_arguments(self, parser):
        """
        Add command arguments to a given parser.

        For consumer and producer subcommands the arguments are inherited directly from Celery worker command. In the
        case of scheduler subcommand, the arguments will also be inherited from Celery beat command.

        :param parser: Argument parser.
        """
        subparsers = parser.add_subparsers(title='Commands', help='Task dispatcher commands')

        wb = worker_bin(app=app)

        parser_consumer = subparsers.add_parser('consumer', help='Run a consumer')
        wb.add_arguments(parser_consumer)
        parser_consumer.set_defaults(func=self.consumer)

        parser_producer = subparsers.add_parser('producer', help='Run a producer')
        wb.add_arguments(parser_producer)
        parser_producer.set_defaults(func=self.producer)

        bb = beat_bin(app=app)

        parser_scheduler = subparsers.add_parser('scheduler', help='Run the tasks scheduler')
        bb.add_arguments(parser_scheduler)
        parser_scheduler.set_defaults(func=self.scheduler)

        parser_register = subparsers.add_parser('list', help='List task registered')
        parser_register.add_argument('-f', '--format', choices=self.LIST_CHOICES, default=self.LIST_YAML)
        parser_register.set_defaults(func=self.list)

    def consumer(self, *args, **kwargs) -> int:
        """
        Run a consumer process.
        """
        kwargs['queues'] = kwargs['queues'] or ['consumer']
        kwargs['hostname'] = kwargs['hostname'] or 'consumer@task-dispatcher'
        worker = app.Worker(**kwargs)
        worker.start()
        return worker.exitcode

    def producer(self, *args, **kwargs) -> int:
        """
        Run a producer process.
        """
        kwargs['queues'] = kwargs['queues'] or ['producer']
        kwargs['hostname'] = kwargs['hostname'] or 'producer@task-dispatcher'
        worker = app.Worker(**kwargs)
        worker.start()
        return worker.exitcode

    def scheduler(self, *args, **kwargs):
        """
        Run a scheduler process.
        """
        beat = app.Beat(**kwargs)
        return beat.run()

    def list(self, *args, **kwargs):
        """
        Lists all producers and consumers registered.
        """
        if kwargs['format'] == self.LIST_YAML:
            print(register.to_yaml())
        else:
            print(register.to_json())

    def run(self, **kwargs):
        """
        Command entrypoint.
        """
        kwargs = kwargs or self.args

        if not kwargs:
            raise ValueError('Arguments must be passed or parsed previously')

        command = kwargs['func']

        return command(**kwargs)
