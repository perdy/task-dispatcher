import sys

from task_dispatcher.decorators import consumer, producer
from task_dispatcher.commands import TaskDispatcherCommand


class A:
    @producer
    def ap(self):
        pass

    @consumer
    def ac(self):
        """
        Test doc.

        :return: Foo.
        """
        pass


@producer(description='Foo')
def p():
    pass


@consumer
def c():
    pass


if __name__ == '__main__':
    sys.exit(TaskDispatcherCommand().run())
