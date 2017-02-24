# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch, MagicMock

import yaml
from celery.app.task import Task
from nose.plugins.attrib import attr

from task_dispatcher.decorators import consumer, producer
from task_dispatcher.register import Register, TaskRegister


class RegisterTestCase(TestCase):
    def setUp(self):
        self.register = Register()

    def test_set_new_item(self):
        self.register['foo'] = 'bar'

        self.assertIn('foo', self.register)
        self.assertEqual(self.register['foo'], 'bar')

    def test_set_existing_item(self):
        self.register['foo'] = 'bar'

        with self.assertRaises(KeyError):
            self.register['foo'] = 'foobar'

    def test_str(self):
        expected_result = str({'foo': 'bar'})

        self.register['foo'] = 'bar'

        self.assertEqual(expected_result, str(self.register))

    def test_repr(self):
        expected_result = repr({'foo': 'bar'})

        self.register['foo'] = 'bar'

        self.assertEqual(expected_result, repr(self.register))


class TaskRegisterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        producer_mock = MagicMock(spec=Task)
        producer_mock.__doc__ = 'docstring'
        producer_mock.__qualname__ = 'qualname'
        producer_mock.__module__ = 'module'
        producer_mock.name = 'producer_name'

        consumer_mock = MagicMock(spec=Task)
        consumer_mock.__doc__ = 'docstring'
        consumer_mock.__qualname__ = 'qualname'
        consumer_mock.__module__ = 'module'
        consumer_mock.name = 'consumer_name'

        with patch('task_dispatcher.decorators.app') as celery_app_mock:
            celery_app_mock.task().side_effect = [producer_mock, consumer_mock]
            cls.tasks = {
                'producer': producer(description='description')(producer_mock),
                'consumer': consumer(consumer_mock)
            }

    def setUp(self):
        self.register = TaskRegister()

    @attr(priority='high', speed='fast')
    def test_register_producer(self):
        self.register.register(self.tasks['producer'])

        self.assertIn(self.tasks['producer'], self.register.producers.values())

    @attr(priority='high', speed='fast')
    def test_register_consumer(self):
        self.register.register(self.tasks['consumer'])

        self.assertIn(self.tasks['consumer'], self.register.consumers.values())

    @attr(priority='high', speed='fast')
    def test_register_unknown(self):
        self.assertRaises(TypeError, self.register.register, False)

    @attr(priority='high', speed='fast')
    def test_consumers(self):
        self.register.register(self.tasks['consumer'])

        self.assertIn(self.tasks['consumer'], self.register.consumers.values())

    @attr(priority='high', speed='fast')
    def test_producers(self):
        self.register.register(self.tasks['producer'])

        self.assertIn(self.tasks['producer'], self.register.producers.values())

    @attr(priority='high', speed='fast')
    def test_to_dict(self):
        expected_result = {
            'consumers': {
                'consumer_name': {
                    'description': 'docstring',
                    'module': 'module',
                    'name': 'qualname',
                },
            },
            'producers': {
                'producer_name': {
                    'description': 'description',
                    'module': 'module',
                    'name': 'qualname',
                }
            }
        }

        self.register.register(self.tasks['consumer'])
        self.register.register(self.tasks['producer'])

        result = self.register.to_dict()

        self.assertDictEqual(expected_result, result)

    @attr(priority='high', speed='fast')
    def test_to_json(self):
        expected_result = json.dumps(OrderedDict(sorted({
            'consumers': {
                'consumer_name': {
                    'description': 'docstring',
                    'module': 'module',
                    'name': 'qualname',
                },
            },
            'producers': {
                'producer_name': {
                    'description': 'description',
                    'module': 'module',
                    'name': 'qualname',
                }
            }
        }.items())))

        self.register.register(self.tasks['consumer'])
        self.register.register(self.tasks['producer'])

        result = self.register.to_json()

        self.assertEqual(expected_result, result)

    @attr(priority='high', speed='fast')
    def test_to_yaml(self):
        expected_result = yaml.safe_dump({
            'consumers': {
                'consumer_name': {
                    'description': 'docstring',
                    'module': 'module',
                    'name': 'qualname',
                },
            },
            'producers': {
                'producer_name': {
                    'description': 'description',
                    'module': 'module',
                    'name': 'qualname',
                }
            }
        }, default_flow_style=False)

        self.register.register(self.tasks['consumer'])
        self.register.register(self.tasks['producer'])

        result = self.register.to_yaml()

        self.assertEqual(expected_result, result)
