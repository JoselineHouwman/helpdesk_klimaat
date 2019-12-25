# Options for the status flow of the question
from django.utils.translation import gettext as _


ASKED = 0       # When the question is just asked, the default
APPROVED = 1    # If the question was approved to be sent to the answering process
ANSWERING = 2   # Once the question gets sent to an expert to answer
REVIEWING = 3   # Once the question was answered and need to get a review
ANSWERED = 4    # Once the question is approved to appear on the website/newsletter, etc

STATUS_CHOICES = (
    (ASKED, _('Asked')),
    (APPROVED, _('Approved')),
    (ANSWERING, _('Answering')),
    (REVIEWING, _('Reviewing')),
    (ANSWERED, _('Answered')),
)
