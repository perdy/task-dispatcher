from functools import partial, update_wrapper

from celery import current_app

from task_dispatcher.register import register

__all__ = ['producer', 'consumer']


class BaseDecorator(object):
    """
    Decorator that creates a Celery task of given function or class method and register it.
    """

    def __init__(self, func=None, description=None, *args, **kwargs):
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

        if func is not None:
            # Full initialization decorator
            self._decorate(func, *args, **kwargs)
        else:
            # Partial initialization decorator
            self.task = None

    def _decorate(self, func, *args, **kwargs):
        self.task = current_app.task(*args, **kwargs)(func)
        update_wrapper(self, func)

        register.list(self)

    def __get__(self, instance, owner=None):
        return partial(self, instance)

    def __getattr__(self, item):
        if self.task:
            return self.task.__getattr__(item)

    def __call__(self, *args, **kwargs):
        if self.task:
            # Decorator behavior
            return self.task(*args, **kwargs)
        else:
            # Decorator is not initialized and now is giving the function to be decorated
            if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
                return self._decorate(func=args[0], *self.args, **self.kwargs)
            else:
                raise ValueError('Decorator is not initialized')


class producer(BaseDecorator):
    """
    Decorator that creates a Celery task of given function or class method and register it. This tasks acts as a
    producer task.
    """
    pass


class consumer(BaseDecorator):
    """
    Decorator that creates a Celery task of given function or class method and register it. This tasks acts as a
    consumer task.
    """
    pass
