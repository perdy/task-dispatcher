===============
Task Dispatcher
===============

:Version: 1.1.0
:Status: Production/Stable
:Author: José Antonio Perdiguero López

Library that provides a system to generate tasks producers and consumers with ease.

Celery is used as backend, so it's necessary to configure it in the application where this library will be used.

To achieve a producer-consumer behavior this library provides an easy to use script for running all necessary processes:

  - **Producer**: Tasks in charge of generating processing units.
  - **Consumer**: Tasks that handle and run processing units.
  - **Scheduler**: Manager that runs producer tasks according to specified dates or regularity.

Quick start
===========

1. Install this package using pip::

    pip install task-dispatcher

2. Decorate your functions as producer and consumer tasks::

    from task_dispatcher import consumer, producer


    @consumer
    def square(x):
        return x**2


    @producer
    def prod_function(n):
        for i in range(n):
            square.delay(i)

3. Run producer, consumer and scheduler processes::

    python task-dispatcher producer
    python task-dispatcher consumer
    python task-dispatcher scheduler

Consumer and Producer
=====================

This library provides convenient decorators for generating a task dispatcher system based on producer-consumer pattern.
Decorated functions or methods acts as Celery tasks and can be called using his own syntax: `Calling celery tasks
<http://docs.celeryproject.org/en/latest/userguide/calling.html>`_. Also, it's possible to compose these tasks using
`Celery Canvas <http://docs.celeryproject.org/en/latest/userguide/canvas.html>`_.

Register
========

Consumer and producer tasks are registered to ease the way of access them. There is a register module that contains the
task register where all tasks can be found::

    from task_dispatcher import register

    # Get consumers
    register.consumers

    # Get produces
    register.producers


Also, this register provides a set of utilities, such as convert it into JSON or YAML format::

    from task_dispatcher import register

    yaml_register = register.to_yaml()
    json_register = register.to_json()

Command Line Interface
======================

There is a script that can be called directly through executing the task_dispatcher package itself or the command
located in commands module. To show command help::

    python task-dispatcher -h

This script also gives a friendly way of list all tasks registered::

    python task-dispatcher list

Django
======

This library can be imported and used as a Django application instead of a plain library, so that the CLI script also
acts as a Django command.