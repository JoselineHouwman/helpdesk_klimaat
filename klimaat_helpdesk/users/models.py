from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, BooleanField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from klimaat_helpdesk.users import USER_ROLES, USER


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    older_13 = BooleanField(_('Older than 13 years'), default=False)
    role = IntegerField(_('User Role'), choices=USER_ROLES, default=USER)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def role_name(self):
        roles = dict(USER_ROLES)
        return roles[self.role]

    def __str__(self):
        return f"{self.name}"


class ExpertProfile(models.Model):
    user = models.OneToOneField(User, related_name='expert_profile', on_delete=models.CASCADE, null=False)
    bio = models.TextField(_('bio'), null=False, blank=True)
    profile_picture = models.FileField(verbose_name=_('Picture'), blank=True)
    areas_expertise = TaggableManager(verbose_name=_('areas of expertise'))
    affiliation = models.CharField(_('Affiliation'), blank=False, max_length=128)
    website = models.URLField(_('Website'), blank=True)
    twitter_profile = models.CharField(_('Twitter Profile'), blank=True, null=True, max_length=50)
    linkedin_profile = models.CharField(_('LinkedIn Profile'), blank=True, null=True, max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user}"


class Expert(models.Model):
    """To split the users from the experts. Users, for the time being will be only those who
    have enough knowledge to interact with the website.
    """
    name = models.CharField(_('name'), max_length=255, null=False, blank=False)
    email = models.EmailField(_('email'), null=True, blank=True)
    bio = models.TextField(verbose_name=_('biography'), null=False, blank=False)
    profile_picture = models.FileField(verbose_name=_('Picture'), blank=True)
    areas_expertise = TaggableManager(verbose_name=_('areas of expertise'))
    affiliation = models.CharField(_('Affiliation'), blank=False, max_length=128)
    website = models.URLField(_('Website'), blank=True)
    twitter_profile = models.CharField(_('Twitter Profile'), blank=True, null=True, max_length=50)
    linkedin_profile = models.CharField(_('LinkedIn Profile'), blank=True, null=True, max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
