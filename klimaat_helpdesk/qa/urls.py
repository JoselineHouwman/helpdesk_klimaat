from django.urls import path
from django.views.generic import TemplateView

from klimaat_helpdesk.qa.views import new_question, editor_home, assign_handler, assign_reviewer, assign_expert, \
    create_answer, review_answer, handler_home, question_details, home_page

app_name = "questions"


urlpatterns = [
    path('', view=home_page, name='home'),
    path('ask', new_question, name='ask'),
    path('ask/thanks', TemplateView.as_view(template_name='qa/new_question_thanks.html'), name='new-question-thanks'),
    path('question', TemplateView.as_view(template_name='question.html'), name='question'),
    path('experts', TemplateView.as_view(template_name='experts.html'), name='experts'),

    path('become-expert', TemplateView.as_view(template_name='become.html'), name='become-expert'),
    path('expert', TemplateView.as_view(template_name='expert_profile.html'), name='expert'),
    path('editor/', view=editor_home, name='editor-home'),
    path('handler/', view=handler_home, name='handler-home'),
    path('question/<int:pk>', view=question_details, name='question-details'),
    path('<int:pk>/assign-handler/', view=assign_handler, name='assign-handler'),
    path('<int:pk>/assign-reviewer/', view=assign_reviewer, name='assign-reviewer'),
    path('<int:pk>/assign-expert', view=assign_expert, name='assign-expert'),
    path('answer/<int:pk>/create', view=create_answer, name='create-answer'),
    path('review/<int:pk>/create', view=review_answer, name='create-review')
]
