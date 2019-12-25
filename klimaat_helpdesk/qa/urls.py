from django.urls import path

from klimaat_helpdesk.qa.views import new_question, list_questions, assign_handler

app_name = "questions"


urlpatterns = [
    path('new/', view=new_question, name='new'),
    path('list/', view=list_questions, name='list'),
    path('assign-handler', view=assign_handler, name='assign-handler')
]
