from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QaConfig(AppConfig):
    name = 'klimaat_helpdesk.qa'
    verbose_name = _('Questions & Answers')
