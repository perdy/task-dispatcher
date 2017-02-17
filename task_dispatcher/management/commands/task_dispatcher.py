# -*- coding: utf-8 -*-
try:
    from django.core.management.base import BaseCommand
except ImportError:
    BaseCommand = object

from task_dispatcher.commands import TaskDispatcherCommand


class Command(BaseCommand):
    """
    Wrapper that makes a Django command from TaskDispatcherCommand.
    """
    help = TaskDispatcherCommand.description

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.command = TaskDispatcherCommand(parse_args=False)

    def add_arguments(self, parser):
        self.command.add_arguments(parser=parser)

    def handle(self, *args, **options):
        self.command.run(**options)
