from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager

from klimaat_helpdesk.qa import STATUS_CHOICES, ASKED

User = get_user_model()


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

    expert = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name=_('Answered by'),
                               related_name='questions_answered')

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name=_('Reviewed by'),
                                 related_name='question_reviews')

    tags = TaggableManager(blank=True)

    # system_tags = TaggableManager(blank=True)  # To store tags such as "need review"

    public = models.BooleanField(default=False, verbose_name=_('public'))

    date_asked = models.DateTimeField(auto_now_add=True)
    date_assigned_handler = models.DateTimeField(null=True, blank=True)
    date_assigned_expert = models.DateTimeField(null=True, blank=True)
    date_answered = models.DateTimeField(null=True, blank=True)
    date_assigned_reviewer = models.DateTimeField(null=True, blank=True)
    date_reviewed = models.DateTimeField(null=True, blank=True)
    date_accepted = models.DateTimeField(null=True, blank=True)

    @property
    def current_status(self):
        statuses = dict(STATUS_CHOICES)
        return statuses[self.status]

    @property
    def last_answer(self):
        return self.answers.last()

    @property
    def last_review(self):
        return self.reviews.last()

    def __str__(self):
        name = self.asked_by or self.asked_by_name or 'anonymous'
        statuses = dict(STATUS_CHOICES)
        status = statuses[self.status]
        return f"Question {self.id} by {name}, current status: {status}"


class Answer(models.Model):
    """ Answers to questions """
    question = models.ForeignKey(Question,
                                 verbose_name=_('question'),
                                 related_name='answers',
                                 on_delete=models.CASCADE,
                                 null=False)

    author = models.ForeignKey(User,
                               verbose_name=_('author'),
                               related_name='answers_given',
                               on_delete=models.CASCADE,
                               null=False)

    answer = models.TextField(verbose_name=_('answer'), blank=False, null=False)
    date_submitted = models.DateTimeField(auto_now_add=False,
                                          default=None,
                                          blank=True,
                                          null=True,
                                          verbose_name=_('date answer submitted'))
    approved = models.BooleanField(default=False, verbose_name=_('answer approved'))

    system_tags = TaggableManager(blank=True)  # To store tags such as "need translation"

    def __str__(self):
        return f"Answer to question {self.question.id} by {self.author.name}"


class Review(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('review'), related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User,
                                 verbose_name=_('reviewer'),
                                 related_name='answer_reviews',
                                 on_delete=models.CASCADE)
    remarks = models.TextField(verbose_name=_('Reviewer remarks'))
    date_submitted = models.DateTimeField(auto_now_add=False,
                                          default=None,
                                          null=True,
                                          blank=True,
                                          verbose_name=_('submission date'))
    approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(auto_now_add=False, default=None, null=True)

    def __str__(self):
        return f"Review to question {self.question.id} by {self.reviewer.name}"
