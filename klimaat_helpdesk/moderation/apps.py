from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ModerationConfig(AppConfig):
    name = 'klimaat_helpdesk.moderation'
    verbose_name = _('Question & Answer Moderation')
