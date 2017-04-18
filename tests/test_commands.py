# -*- coding: utf-8 -*-
import os
from unittest.case import TestCase
from unittest.mock import patch, call, MagicMock

from clinner.exceptions import ImproperlyConfigured
from clinner.settings import settings
from nose.plugins.attrib import attr

from task_dispatcher.commands import TaskDispatcherCommand, consumer, producer, scheduler, show, flower
from task_dispatcher.management.commands.task_dispatcher import Command


class TaskDispatcherCommandTestCase(TestCase):
    def setUp(self):
        os.environ['TASK_DISPATCHER_SETTINGS'] = ''

    @attr(priority='mid', speed='fast')
    def test_consumer(self):
        expected_kwarg = 'queues'
        expected_queues = ['consumer']

        with patch('task_dispatcher.commands.app') as celery_app_mock:
            consumer(queues=None)

        self.assertEqual(celery_app_mock.Worker.call_count, 1)
        self.assertIn(expected_kwarg, celery_app_mock.Worker.call_args[1])
        self.assertCountEqual(expected_queues, celery_app_mock.Worker.call_args[1]['queues'])

    @attr(priority='mid', speed='fast')
    def test_producer(self):
        expected_kwarg = 'queues'
        expected_queues = ['producer']

        with patch('task_dispatcher.commands.app') as celery_app_mock:
            producer(queues=None)

        self.assertEqual(celery_app_mock.Worker.call_count, 1)
        self.assertIn(expected_kwarg, celery_app_mock.Worker.call_args[1])
        self.assertCountEqual(expected_queues, celery_app_mock.Worker.call_args[1]['queues'])

    @attr(priority='mid', speed='fast')
    def test_scheduler(self):
        task = 'foo'
        task_args = (1, 2)
        task_kwargs = {'foo', 'bar'}
        expected_calls = [call(task, args=task_args, kwargs=task_kwargs)]

        with patch('task_dispatcher.commands.app') as celery_app_mock, \
                patch('task_dispatcher.commands.settings') as task_dispatcher_settings:
            task_dispatcher_settings.run_at_startup = [(task, task_args, task_kwargs)]
            scheduler()

            self.assertCountEqual(celery_app_mock.send_task.call_args_list, expected_calls)

        self.assertEqual(celery_app_mock.Beat.call_count, 1)

    @attr(priority='mid', speed='fast')
    @patch('task_dispatcher.commands.app')
    def test_flower(self, celery_app_mock):
        expected_calls = [call(app=celery_app_mock)]
        expected_calls_cmdline = [call(argv=('flower',))]

        with patch('task_dispatcher.commands.FlowerCommand') as flower_mock:
            flower()

        self.assertEqual(flower_mock.call_count, 1)
        self.assertEqual(flower_mock.call_args_list, expected_calls)

        self.assertEqual(flower_mock().execute_from_commandline.call_count, 1)
        self.assertEqual(flower_mock().execute_from_commandline.call_args_list, expected_calls_cmdline)

    @attr(priority='mid', speed='fast')
    def test_show_yaml(self):
        with patch('task_dispatcher.commands.register') as register_mock:
            show(format='yaml')

        self.assertEqual(register_mock.to_yaml.call_count, 1)

    @attr(priority='mid', speed='fast')
    def test_show_json(self):
        with patch('task_dispatcher.commands.register') as register_mock:
            show(format='json')

        self.assertEqual(register_mock.to_json.call_count, 1)

    @attr(priority='low', speed='fast')
    def test_run_no_args(self):
        command = TaskDispatcherCommand(parse_args=False)

        self.assertRaises(Exception, command.run)

    @attr(priority='low', speed='fast')
    def test_inject_settings(self):
        with patch.object(settings, 'build_from_module'):
            TaskDispatcherCommand(['-s', 'foo', 'show'])

    @attr(priority='low', speed='fast')
    def test_inject_settings_fails(self):
        del os.environ['TASK_DISPATCHER_SETTINGS']
        with self.assertRaises(ImproperlyConfigured):
            TaskDispatcherCommand(['show'])

    @attr(priority='low', speed='fast')
    def test_django_command(self):
        with patch('task_dispatcher.management.commands.task_dispatcher.TaskDispatcherCommand') as command_mock:
            parser_mock = MagicMock()
            command = Command()
            command.add_arguments(parser_mock)
            command.handle(foo='bar')

            self.assertEqual(command_mock.call_count, 1)
            self.assertEqual(command_mock()._add_arguments.call_count, 1)
            self.assertEqual(command_mock().run.call_args_list, [call(foo='bar')])
