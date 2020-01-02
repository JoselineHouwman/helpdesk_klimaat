from django.contrib import admin

from klimaat_helpdesk.qa.models import Question, Answer, Review, Category

admin.site.register((Question, Answer, Review, Category))
