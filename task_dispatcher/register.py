# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

import yaml

__all__ = ['register', 'TaskRegister', 'Register']


class Register(dict):
    """
    Special case of dictionary that when keys cannot be replaced.
    """
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError('{} is already registered'.format(key))

        dict.__setitem__(self, key, value)

    def __repr__(self):
        return dict.__repr__(self)

    def __str__(self):
        return dict.__str__(self)


class TaskRegister:
    """
    Register for producer and consumer tasks.
    """
    def __init__(self):
        """
        Register for producer and consumer tasks.
        """
        self._producers = Register()
        self._consumers = Register()

    def register(self, item):
        """
        Register a new task. The task will be discriminated and stored in their assigned register.

        :param item: Task to be registered.
        :raise TypeError: Item is not a registrable task.
        """
        from task_dispatcher.decorators import producer, consumer

        if isinstance(item, producer):
            self._producers[item.name] = item
        elif isinstance(item, consumer):
            self._consumers[item.name] = item
        else:
            raise TypeError(item)

    @property
    def producers(self):
        """
        Producers register.

        :return: Producers register.
        """
        return self._producers

    @property
    def consumers(self):
        """
        Consumers register.

        :return: Consumers register.
        """
        return self._consumers

    def to_dict(self) -> dict:
        """
        Transform the task register to a dictionary.

        :return: Task register transformed.
        """
        def get_description(task):
            return {
                'description': task.description or task.__doc__ or 'Description not found',
                'module': task.__module__,
                'name': task.__qualname__,
            }

        return OrderedDict([
            ('consumers', {k: get_description(v) for k, v in self._consumers.items()}),
            ('producers', {k: get_description(v) for k, v in self._producers.items()}),
        ])

    def to_json(self) -> str:
        """
        Transform the task register to a JSON string.

        :return: Task register transformed.
        """
        return json.dumps(self.to_dict())

    def to_yaml(self) -> str:
        """
        Transform the task register to a YAML string.

        :return: Task register transformed.
        """
        return yaml.dump(dict(self.to_dict()), default_flow_style=False)


register = TaskRegister()
