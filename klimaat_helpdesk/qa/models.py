from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager

from klimaat_helpdesk.qa import STATUS_CHOICES, ASKED, APPROVED
from klimaat_helpdesk.qa.managers import QuestionManager
from klimaat_helpdesk.users.models import Expert

User = get_user_model()


class TemporaryQuestion(models.Model):
    """Temporary Questions are those questions asked by users and waiting to be moderated. They hold the information
    submitted by the users.
    """
    question = models.TextField(_('Question'), null=False, blank=False)
    asked_by = models.EmailField(_('Email'), null=True, blank=True)
    asked_by_ip = models.GenericIPAddressField(null=True, blank=True)
    asked_date = models.DateTimeField(auto_now_add=True)
    over_13 = models.BooleanField(_('Older than 13 years'), default=False)

    approved = models.NullBooleanField(default=None, null=True)

    rejection = models.TextField(_('Rejection reason'), null=True, blank=False)

    objects = QuestionManager()

    def approve(self, user):
        """Copies the relevant information to a new Question and also keeps track of who approved the question"""
        question = Question.objects.create(
            question=self.question,
            asked_by_email=self.asked_by,
            status=APPROVED,
            approved_by=user,
        )
        self.approved = True
        self.save()
        return question

    def reject(self):
        self.approved = False
        self.save()

    def __str__(self):
        if self.approved:
            status = "Approved"
        elif self.approved is None:
            status = "Waiting decision"
        else:
            status = "Rejected"

        return f"Question {self.pk} - {status}"


class Question(models.Model):
    """ This model is the core of the application. Each question marks the flow of the application from the moment
    where it was asked until the moment it is published on the website.
    """
    title = models.CharField(_('Title'), null=True, blank=True, max_length=255)
    question = models.TextField(verbose_name=_('Question'), null=False, blank=False)

    asked_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='questions',
                                 verbose_name=_('Asked by'))

    asked_by_email = models.EmailField(_('Email'), null=True, blank=True)

    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=ASKED)

    approved_by = models.ForeignKey(User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    verbose_name=_('Approved by'),
                                    related_name='questions_approved')

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

    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='articles',
                                 verbose_name=_('category'))

    public = models.BooleanField(default=False, verbose_name=_('public'))

    date_asked = models.DateTimeField(auto_now_add=True)
    date_assigned_handler = models.DateTimeField(null=True, blank=True)
    date_assigned_expert = models.DateTimeField(null=True, blank=True)
    date_answered = models.DateTimeField(null=True, blank=True)
    date_assigned_reviewer = models.DateTimeField(null=True, blank=True)
    date_reviewed = models.DateTimeField(null=True, blank=True)
    date_accepted = models.DateTimeField(null=True, blank=True)
    date_published = models.DateTimeField(null=True, blank=True)

    objects = QuestionManager()

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
        name = self.asked_by or self.asked_by_email or 'anonymous'
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


class Category(models.Model):
    name = models.CharField(_('name'), max_length=255, null=False, blank=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=False, null=False)
    text = models.TextField(blank=False, null=False)

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_('created by'))
    expert = models.ForeignKey(Expert, on_delete=models.DO_NOTHING, blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    public = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.updated_date = now()
        super(Article, self).save(**kwargs)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    class Meta:
        ordering = ['-creation_date']
