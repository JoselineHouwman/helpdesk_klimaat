from logging import getLogger

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView, ListView, UpdateView, DetailView

from klimaat_helpdesk.qa.forms import AddNewQuestion
from klimaat_helpdesk.qa.models import Question, Answer, Review
from klimaat_helpdesk.users import HANDLER, EXPERT, REVIEWER

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

        Question.objects.create(
            question=form.cleaned_data['question'],
            asked_by_name=form.cleaned_data['name'],
            asked_by=user,
        )
        name = form.cleaned_data['name'] or 'Anonymous'
        logger.info(f'Added new question by {name}')
        return super(NewQuestion, self).form_valid(form)


new_question = NewQuestion.as_view()


class EditorHomeView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qa/editor_home.html'


editor_home = EditorHomeView.as_view()


class HandlerHomeView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qa/handler_home.html'


handler_home = HandlerHomeView.as_view()


class AssignHandlerView(UpdateView):
    model = Question
    fields = ['handler', ]
    template_name = 'qa/assign_handler.html'
    success_url = reverse_lazy('questions:list')
    context_object_name = 'question'

    def get_form(self, *args, **kwargs):
        form = super(AssignHandlerView, self).get_form(*args, **kwargs)
        form.fields['handler'].queryset = User.objects.filter(role__gte=HANDLER)
        return form

    def form_valid(self, form):
        self.object.date_assigned_handler = now()
        self.object.save()
        return super(AssignHandlerView, self).form_valid(form)


assign_handler = AssignHandlerView.as_view()


class AssignExpert(UpdateView):
    model = Question
    fields = ['expert', ]
    template_name = 'qa/assign_expert.html'
    success_url = reverse_lazy('questions:list')

    def get_form(self, *args, **kwargs):
        form = super(AssignExpert, self).get_form(*args, **kwargs)
        form.fields['expert'].queryset = User.objects.filter(role__gte=EXPERT)
        return form

    def form_valid(self, form):
        self.object.date_assigned_expert = now()
        self.object.save()
        Answer.objects.create(
            question=self.object,
            author=form.cleaned_data['expert']
        )

        return super(AssignExpert, self).form_valid(form)


assign_expert = AssignExpert.as_view()


class AssignReviewer(UpdateView):
    model = Question
    fields = ['reviewer', ]
    template_name = 'qa/assign_reviewer.html'
    success_url = reverse_lazy('questions:list')

    def get_form(self, *args, **kwargs):
        form = super(AssignReviewer, self).get_form(*args, **kwargs)
        form.fields['reviewer'].queryset = User.objects.filter(role__gte=REVIEWER)
        return form

    def form_valid(self, form):
        self.object.date_assigned_reviewer = now()
        self.object.save()
        Review.objects.create(
            question=self.object,
            reviewer=form.cleaned_data['reviewer']
        )

        return super(AssignReviewer, self).form_valid(form)


assign_reviewer = AssignReviewer.as_view()


class CreateAnswer(UpdateView):
    model = Answer
    fields = ['answer', ]
    context_object_name = 'answer'
    template_name = 'qa/create_answer.html'
    success_url = '/'

    def form_valid(self, form):
        self.object.date_submitted = now()
        self.object.save()
        return super(CreateAnswer, self).form_valid(form)


create_answer = CreateAnswer.as_view()


class ReviewAnswer(UpdateView):
    model = Review
    fields = ['remarks', ]
    context_object_name = 'review'
    template_name = 'qa/create_review.html'
    success_url = '/'

    def form_valid(self, form):
        self.object.date_submitted = now()
        self.object.save()
        return super(ReviewAnswer, self).form_valid(form)


review_answer = ReviewAnswer.as_view()


class QuestionDetails(UpdateView):
    model = Question
    template_name = 'qa/question_details.html'

    fields = '__all__'

    def get_success_url(self):
        return self.request.path


question_details = QuestionDetails.as_view()