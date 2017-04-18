# -*- coding: utf-8 -*-
import os
import sys

sys.path[0] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

from task_dispatcher.commands import TaskDispatcherCommand  # noqa

__all__ = ['main']


def main():
    return TaskDispatcherCommand().run()


if __name__ == '__main__':
    sys.exit(main())
