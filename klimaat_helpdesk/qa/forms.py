from django import forms
from django.utils.translation import gettext as _


class AddNewQuestion(forms.Form):
    name = forms.CharField(label=_('Your name'), max_length=255, required=False)
    email = forms.EmailField(label=_('Your email'), required=False, help_text=_('If you want to be updated about your question'))
    question = forms.CharField(label=_('Your question'), required=True, widget=forms.Textarea)
