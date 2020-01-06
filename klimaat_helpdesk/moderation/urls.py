from django.urls import path

from klimaat_helpdesk.moderation.views import new_questions_list, approve_question, assign_handler, question_handling, \
    reject_question, assign_expert, create_expert, create_expert_profile

app_name = "moderation"


urlpatterns = [
    path('', new_questions_list, name='new-questions'),
    path('approve/<int:pk>', approve_question, name='approve'),
    path('reject/<int:pk>', reject_question, name='reject'),
    path('assign-handler/<int:pk>', assign_handler, name='assign-handler'),
    path('handling', question_handling, name='handling'),
    path('assign-expert/<int:pk>', assign_expert, name='assign-expert'),
    path('create-expert', create_expert, name='create-expert'),
    path('create-expert-profile/<int:pk>', create_expert_profile, name='create-expert-profile'),
]
