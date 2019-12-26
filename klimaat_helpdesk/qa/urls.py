from django.urls import path

from klimaat_helpdesk.qa.views import new_question, editor_home, assign_handler, assign_reviewer, assign_expert, \
    create_answer, review_answer, handler_home, question_details

app_name = "questions"


urlpatterns = [
    path('', view=new_question, name='home'),
    path('editor/', view=editor_home, name='editor-home'),
    path('handler/', view=handler_home, name='handler-home'),
    path('question/<int:pk>/details', view=question_details, name='question-details'),
    path('<int:pk>/assign-handler/', view=assign_handler, name='assign-handler'),
    path('<int:pk>/assign-reviewer/', view=assign_reviewer, name='assign-reviewer'),
    path('<int:pk>/assign-expert', view=assign_expert, name='assign-expert'),
    path('answer/<int:pk>/create', view=create_answer, name='create-answer'),
    path('review/<int:pk>/create', view=review_answer, name='create-review')
]
