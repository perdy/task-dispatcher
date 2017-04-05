# -*- coding: utf-8 -*-
from unittest.case import TestCase
from unittest.mock import MagicMock, patch, call

from celery.app.task import Task
from nose.plugins.attrib import attr

from task_dispatcher.decorators import BaseDecorator


class TestMock(MagicMock):
    def foo_method(self, x):
        return x


class BaseDecoratorTestCase(TestCase):
    def setUp(self):
        self.task_mock = TestMock(spec=Task)
        self.task_mock.__doc__ = 'docstring'
        self.task_mock.__qualname__ = 'qualname'
        self.task_mock.__module__ = 'module'
        self.task_mock.name = 'task_name'

    @attr(priority='high', speed='fast')
    def test_full_initialize_without_args(self):
        with patch.object(BaseDecorator, '_decorate') as decorate_mock:
            BaseDecorator(self.task_mock)
            self.assertEqual(decorate_mock.call_count, 1)

    @attr(priority='high', speed='fast')
    def test_partial_initialize_with_args(self):
        with patch.object(BaseDecorator, '_decorate') as decorate_mock:
            # Partial initialization to pass description
            decorator = BaseDecorator(description='description')

            self.assertEqual(decorate_mock.call_count, 0)

            # Full initialization through __call__
            decorator(self.task_mock)

            self.assertEqual(decorate_mock.call_count, 1)

    @attr(priority='high', speed='fast')
    def test_get(self):
        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            celery_app_mock.task().return_value = self.task_mock

            decorator = BaseDecorator(self.task_mock)

        self.assertTrue(isinstance(decorator.__get__(decorator), BaseDecorator))
        self.assertEqual(decorator.instance, decorator)

    @attr(priority='high', speed='fast')
    def test_getattr_decorator_attr(self):
        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            celery_app_mock.task().return_value = self.task_mock

            decorator = BaseDecorator(description='description')(self.task_mock)

        description = decorator.description
        expected_description = 'description'

        self.assertEqual(expected_description, description)

    @attr(priority='high', speed='fast')
    def test_getattr_task_attr(self):
        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            celery_app_mock.task().return_value = self.task_mock

            decorator = BaseDecorator(description='description')(self.task_mock)

        decorator.task.foo = 'bar'
        name = decorator.foo
        expected_name = 'bar'

        self.assertEqual(expected_name, name)

    @attr(priority='high', speed='fast')
    def test_getattr_task_method(self):
        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            celery_app_mock.task().return_value = self.task_mock

            decorator = BaseDecorator(description='description')(self.task_mock)

        name = decorator.foo_method('bar')
        expected_name = 'bar'

        self.assertEqual(expected_name, name)

    @attr(priority='high', speed='fast')
    def test_decorate(self):
        expected_task_name = '.'.join([self.task_mock.__module__, self.task_mock.__qualname__])

        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            celery_app_mock.task().return_value = self.task_mock

            decorator = BaseDecorator(self.task_mock)

            self.assertEqual(self.task_mock, decorator.task)
            self.assertEqual(register_mock.register.call_count, 1)
            self.assertIn('name', celery_app_mock.task.call_args[1])
            self.assertEqual(celery_app_mock.task.call_args[1]['name'], expected_task_name)

    @attr(priority='high', speed='fast')
    def test_call(self):
        expected_call_args = [call('foo', bar='bar')]

        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            # Partial initialization to pass description
            celery_app_mock.task().return_value = self.task_mock
            decorator = BaseDecorator(description='description')(self.task_mock)

            # Full initialization through __call__
            decorator('foo', bar='bar')

            self.assertEqual(self.task_mock, decorator.task)
            self.assertEqual(self.task_mock.call_count, 1)
            self.assertCountEqual(expected_call_args, self.task_mock.call_args_list)

    @attr(priority='high', speed='fast')
    def test_call_not_initialized(self):
        with patch('task_dispatcher.decorators.app') as celery_app_mock, \
                patch('task_dispatcher.decorators.register') as register_mock:
            # Partial initialization to pass description
            celery_app_mock.task().return_value = self.task_mock
            decorator = BaseDecorator(description='description')

            # Try to call before full initialization
            self.assertRaises(ValueError, decorator, 'foo', bar='bar')

    @attr(priority='high', speed='fast')
    def test_getattr_without_task(self):
        decorator = BaseDecorator()

        with self.assertRaises(AttributeError):
            _ = getattr(decorator, 'foo')
