from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager

from klimaat_helpdesk.qa import STATUS_CHOICES, ASKED


class Question(models.Model):
    """ This model is the core of the application. Each question marks the flow of the application from the moment
    where it was asked until the moment it is published on the website.
    """
    question = models.TextField(verbose_name=_('Question'), null=False, blank=False)

    asked_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='questions',
                                 verbose_name=_('Asked by'))

    asked_by_name = models.CharField(max_length=255,
        verbose_name=_('Name of the person asking'),
        null=True,
        blank=True,
        help_text='In case there is name but no e-mail')

    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=ASKED)

    handler = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                verbose_name=_('Handler'),
                                related_name='handling')

    answerer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name=_('Answered by'),
                                 related_name='answers')

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name=_('Reviewd by'),
                                 related_name='reviews')

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

    def __str__(self):
        name = self.asked_by or self.asked_by_name or 'anonymous'
        statuses = dict(STATUS_CHOICES)
        status = statuses[self.status]
        return f"Question {self.id} by {name}, current status: {status}"
