from django.contrib.auth import get_user_model, forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _

from klimaat_helpdesk.users import EXPERT
from klimaat_helpdesk.users.models import ExpertProfile

User = get_user_model()


class ExpertCreationForm(forms.Form):
    name = forms.CharField(max_length=255, label=_('name'), required=True)
    email = forms.EmailField(label=_('email'), required=True)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('That e-mail is already on our database'))
        return email

    def save(self, commit=True):
        user = User.objects.create(
            name=self.cleaned_data['name'],
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            role=EXPERT,
        )
        ExpertProfile.objects.create(
            user=user
        )
        return user
