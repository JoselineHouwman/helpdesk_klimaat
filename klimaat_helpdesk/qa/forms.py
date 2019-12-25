from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from klimaat_helpdesk.users import HANDLER

User = get_user_model()

class AddNewQuestion(forms.Form):
    name = forms.CharField(label=_('Your name'),
                           max_length=255,
                           required=False,
                           help_text=_('Only if you would like to share your name with us'))

    email = forms.EmailField(label=_('Your email'),
                             required=False,
                             help_text=_('If you want to be updated about your question'))

    question = forms.CharField(label=_('Your question'),
                               required=True,
                               widget=forms.Textarea)

    under_13 = forms.BooleanField(label=_('Older than 13 years'), required=False)

    accept_privacy = forms.BooleanField(required=True)


class AssignHandler(forms.Form):
    queryset = User.objects.filter(role=HANDLER)
    handler = forms.ModelChoiceField(queryset)
