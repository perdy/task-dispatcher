"""Django application config module.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TaskDispatcher(AppConfig):
    name = 'task_dispatcher'
    verbose_name = _('Task Dispatcher')
