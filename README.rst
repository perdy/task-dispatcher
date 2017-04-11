===============
Task Dispatcher
===============

|build-status| |coverage|

:Version: 1.2.2
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

1. Install this package using pip:

.. code:: bash

    pip install task-dispatcher

2. Decorate your functions as producer and consumer tasks:

.. code:: python

    from task_dispatcher import consumer, producer


    @consumer
    def square(x):
        return x**2


    @producer
    def prod_function(n):
        for i in range(n):
            square.delay(i)

3. Run producer, consumer and scheduler processes:

.. code:: bash

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
task register where all tasks can be found:

.. code:: python

    from task_dispatcher import register

    # Get consumers
    register.consumers

    # Get produces
    register.producers


Also, this register provides a set of utilities, such as convert it into JSON or YAML format:

.. code:: python

    from task_dispatcher import register

    yaml_register = register.to_yaml()
    json_register = register.to_json()

Command Line Interface
======================

There is a script that can be called directly through executing the task_dispatcher package itself or the command
located in commands module. To show command help:

.. code:: bash

    python task-dispatcher -h

This script also gives a friendly way of list all tasks registered:

.. code:: bash

    python task-dispatcher list

Django
======

This library can be imported and used as a Django application instead of a plain library, so that the CLI script also
acts as a Django command.

Settings
========

Celery settings can be specified through **TASK_DISPATCHER_SETTINGS** variable using path format indicated in
`Celery application configuration <http://docs.celeryproject.org/en/latest/userguide/application.html#configuration>`_.


.. |build-status| image:: https://travis-ci.org/PeRDy/task-dispatcher.svg?branch=master
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/PeRDy/task-dispatcher
.. |coverage| image:: https://coveralls.io/repos/github/PeRDy/task-dispatcher/badge.svg
    :alt: coverage
    :scale: 100%
    :target: https://coveralls.io/github/PeRDy/task-dispatcher
