from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager

from klimaat_helpdesk.qa import STATUS_CHOICES, ASKED


class Question(models.Model):
    """ This model is the core of the application. Each question marks the flow of the application from the moment
    where it was asked until the moment it is published on the website.
    """
    question = models.TextField(_('Question'), null=False, blank=False)
    asked_by = models.ForeignKey(_('Asked by'), settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    asked_by_name = models.CharField(_('Name of the person asking'), null=True, blank=True, help_text='In case there is name but no e-mail')
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=ASKED)
    handler = models.ForeignKey(_('Handler'), settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    answerer = models.ForeignKey(_('Answered by'), settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(_('Reviewd by'), settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True)
    tags = TaggableManager()

    date_asked = models.DateTimeField(auto_now_add=True)
    date_assigned_handler = models.DateTimeField(null=True)
    date_assigned_answerer = models.DateTimeField(null=True)
    date_answered = models.DateTimeField(null=True)
    date_assigned_reviewer = models.DateTimeField(null=True)
    date_reviewed = models.DateTimeField(null=True)
    date_accepted = models.DateTimeField(null=True)

    @property
    def current_status(self):
        statuses = dict(STATUS_CHOICES)
        return statuses[self.status]


