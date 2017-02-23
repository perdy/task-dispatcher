# -*- coding: utf-8 -*-
"""Django application config module.
"""
try:
    from django.apps import AppConfig
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    AppConfig = object

    def _(x): return x


class TaskDispatcher(AppConfig):
    name = 'task_dispatcher'
    verbose_name = _('Task Dispatcher')
