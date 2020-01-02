from django.db import models

from klimaat_helpdesk.qa import ANSWERED


class QuestionManager(models.Manager):
    def waiting_approval(self):
        return super().get_queryset().filter(approved=None)

    def approved(self):
        return super().get_queryset().filter(approved=True)

    def rejected(self):
        return super().get_queryset().filter(approved=False)

    def more_recent(self, n):
        """Get the n more recent questions"""
        return super().get_queryset().filter(status=ANSWERED).order_by('-date_published')
