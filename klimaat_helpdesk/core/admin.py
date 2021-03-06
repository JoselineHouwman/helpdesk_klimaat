from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from django.utils.translation import ugettext_lazy as _
from klimaat_helpdesk.core.models import Question


class QuestionAdmin(ModelAdmin):
    model = Question
    menu_label = _('Questions')
    menu_icon = 'help'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('question', 'user_email', 'date_asked', 'approved')
    search_fields = ("user_email", "question")


modeladmin_register(QuestionAdmin)
