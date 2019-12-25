from logging import getLogger

from django.contrib.auth import get_user_model
from django.views.generic import FormView, ListView

from klimaat_helpdesk.qa.forms import AddNewQuestion, AssignHandler
from klimaat_helpdesk.qa.models import Question

User = get_user_model()

logger = getLogger(__name__)

class NewQuestion(FormView):
    form_class = AddNewQuestion
    template_name = 'qa/new_question.html'
    success_url = '/'

    def form_valid(self, form):
        user = None
        if form.cleaned_data['email']:
            user, created = User.objects.get_or_create(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'])

        question = Question.objects.create(
            question=form.cleaned_data['question'],
            asked_by_name=form.cleaned_data['name'],
            asked_by=user,
        )
        name = form.cleaned_data['name'] or 'Anonymous'
        logger.info(f'Added new question by {name}')
        return super(NewQuestion, self).form_valid(form)


new_question = NewQuestion.as_view()


class ListQuestions(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qa/list_question.html'


list_questions = ListQuestions.as_view()


class AssignHandlerView(FormView):
    form_class = AssignHandler
    template_name = 'qa/assign_handler.html'
    success_url = '/'


assign_handler = AssignHandlerView.as_view()
