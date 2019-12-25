from django.utils.translation import ugettext_lazy as _


USER = 1        # General user, who can ask
EXPERT = 2      # Expert, who can answer
REVIEWER = 3    # Reviewer, who can also answer
HANDLER = 4     # Those who can handle answers, contact the reviewers, etc.
EDITOR = 5      # Assign handlers, can override decisions


USER_ROLES = (
    (USER, _('User')),
    (EXPERT, _('Expert')),
    (REVIEWER, _('Reviewer')),
    (EDITOR, _('Editor')),
)
