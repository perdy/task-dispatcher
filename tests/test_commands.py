# -*- coding: utf-8 -*-
import sys
from unittest.case import TestCase
from unittest.mock import patch

from nose.plugins.attrib import attr

from task_dispatcher.commands import TaskDispatcherCommand


class TaskDispatcherCommandTestCase(TestCase):
    @attr(priority='mid', speed='fast')
    def test_consumer(self):
        expected_kwarg = 'queues'
        expected_queues = ['consumer']

        sys.argv = ['command', 'consumer']
        command = TaskDispatcherCommand()

        with patch('task_dispatcher.commands.app') as celery_app_mock:
            command.run()

        self.assertEqual(celery_app_mock.Worker.call_count, 1)
        self.assertIn(expected_kwarg, celery_app_mock.Worker.call_args[1])
        self.assertCountEqual(expected_queues, celery_app_mock.Worker.call_args[1]['queues'])

    @attr(priority='mid', speed='fast')
    def test_producer(self):
        expected_kwarg = 'queues'
        expected_queues = ['producer']

        sys.argv = ['command', 'producer']
        command = TaskDispatcherCommand()

        with patch('task_dispatcher.commands.app') as celery_app_mock:
            command.run()

        self.assertEqual(celery_app_mock.Worker.call_count, 1)
        self.assertIn(expected_kwarg, celery_app_mock.Worker.call_args[1])
        self.assertCountEqual(expected_queues, celery_app_mock.Worker.call_args[1]['queues'])

    @attr(priority='mid', speed='fast')
    def test_scheduler(self):
        sys.argv = ['command', 'scheduler']
        command = TaskDispatcherCommand()

        with patch('task_dispatcher.commands.app') as celery_app_mock:
            command.run()

        self.assertEqual(celery_app_mock.Beat.call_count, 1)

    @attr(priority='mid', speed='fast')
    def test_list_yaml(self):
        sys.argv = ['command', 'list']
        command = TaskDispatcherCommand()

        with patch('task_dispatcher.commands.register') as register_mock:
            command.run()

        self.assertEqual(register_mock.to_yaml.call_count, 1)

    @attr(priority='mid', speed='fast')
    def test_list_json(self):
        sys.argv = ['command', 'list', '-f', 'json']
        command = TaskDispatcherCommand()

        with patch('task_dispatcher.commands.register') as register_mock:
            command.run()

        self.assertEqual(register_mock.to_json.call_count, 1)

    @attr(priority='low', speed='fast')
    def test_run_no_args(self):
        command = TaskDispatcherCommand(parse_args=False)

        self.assertRaises(ValueError, command.run)
