from django.urls import path

from klimaat_helpdesk.moderation.views import new_questions_list, approve_question, assign_handler, question_handling, \
    reject_question

app_name = "moderation"


urlpatterns = [
    path('', new_questions_list, name='new-questions'),
    path('approve/<int:pk>', approve_question, name='approve'),
    path('reject/<int:pk>', reject_question, name='reject'),
    path('assign-handler/<int:pk>', assign_handler, name='assign-hanlder'),
    path('handling', question_handling, name='handling'),
]
