# -*- coding: utf-8 -*-
import sys

from task_dispatcher.commands import TaskDispatcherCommand

__all__ = ['main']


def main():
    return TaskDispatcherCommand().run()


if __name__ == '__main__':
    sys.exit(main())
