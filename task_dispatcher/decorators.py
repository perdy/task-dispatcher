# -*- coding: utf-8 -*-
import inspect
from functools import partial
from functools import update_wrapper
from typing import Callable

from task_dispatcher.celery import app
from task_dispatcher.register import register

__all__ = ['producer', 'consumer']


class BaseDecorator(object):
    """
    Decorator that creates a Celery task of given function or class method and register it.

    When subclassing BaseDecorator, class attribute 'default_queue' can be defined to specify the default queue name
    for the tasks being decorated.
    """

    def __init__(self, func: Callable=None, description: str=None, *args, **kwargs):
        """
        Decorator that creates a Celery task of given function or class method and register it. This decorator allows
        to be used as a common decorator without arguments:

        @BaseDecorator
        def foo(bar):
            pass

        But also is possible to provide some arguments, such as a task description:
        @BaseDecorator(description='Foo task that does nothing')
        def foo(bar):
            pass

        It's also possible to pass arguments to Celery task decorator, e.g:
        @BaseDecorator(queue='base_queue')
        def foo(bar):
            pass

        For last, is possible to decorate functions or class methods:
        class Foo:
            @BaseDecorator
            def bar(self):
                pass

        :param func: Function or class method to be decorated.
        :param description: Task description.
        :param args: Celery task args.
        :param kwargs: Celery task kwargs.
        """
        self.description = description
        self.args = args
        self.kwargs = kwargs
        self.task = None
        self.instance = None

        if func is not None:
            # Full initialization decorator
            self._decorate(func, *args, **kwargs)

    def _decorate(self, func: Callable, *args, **kwargs):
        # Default name as the function's fully qualified name
        kwargs['name'] = kwargs.get('name', '.'.join([func.__module__, func.__qualname__]))

        # Default queue
        if hasattr(self, 'default_queue'):
            kwargs['queue'] = kwargs.get('queue', self.default_queue)

        self.task = app.task(*args, **kwargs)(func)
        update_wrapper(self, func)

        register.register(self)

    def __get__(self, instance, owner=None):
        """
        Make it works with functions and methods.
        """
        self.instance = instance
        return self

    def __getattr__(self, item):
        """
        Make this decorator a simple proxy for task instance.
        """
        # If looking for an unknown attr, delegates it to task __getattr__
        if self.task:
            if self.instance and inspect.ismethod(getattr(self.task, item)):
                return partial(getattr(self.task, item), self.instance)
            else:
                return getattr(self.task, item)
        else:
            raise AttributeError

    def __call__(self, *args, **kwargs):
        """
        Redirect calls to task instance. If decorator is not fully initialized, initialize it.
        """
        if self.task:
            # Decorator behavior
            if self.instance:
                return self.task(self.instance, *args, **kwargs)
            else:
                return self.task(*args, **kwargs)
        else:
            # Decorator is not initialized and now is giving the function to be decorated
            if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
                self._decorate(func=args[0], *self.args, **self.kwargs)
                return self
            else:
                raise ValueError('Decorator is not initialized')


class producer(BaseDecorator):  # noqa
    """
    Decorator that creates a Celery task of given function or class method and register it. This tasks acts as a
    producer task.
    """
    default_queue = 'producer'


class consumer(BaseDecorator):  # noqa
    """
    Decorator that creates a Celery task of given function or class method and register it. This tasks acts as a
    consumer task.
    """
    default_queue = 'consumer'
