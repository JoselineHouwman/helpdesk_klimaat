from django import forms
from django.contrib.auth import get_user_model, forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from klimaat_helpdesk.users import USER_ROLES

User = get_user_model()


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(auth_forms.UserCreationForm):

    error_message = auth_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class CreateUser(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=255, required=True)
    email = forms.EmailField(label=_('Email'), required=True)
    role = forms.ChoiceField(label=_('Role'), required=True, choices=USER_ROLES)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                return email
            user.email = email
            user.save()

        raise ValidationError(_('This email is already present on the database'))


