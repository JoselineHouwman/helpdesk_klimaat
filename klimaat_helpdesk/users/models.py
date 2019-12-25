from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from klimaat_helpdesk.users import USER_ROLES, USER


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    older_13 = BooleanField(_('Older than 13 years'), default=False)
    role = IntegerField(_('User Role'), choices=USER_ROLES, default=USER)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
