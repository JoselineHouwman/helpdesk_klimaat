from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, UpdateView
from django.views.generic.base import View

from klimaat_helpdesk.qa.models import TemporaryQuestion, Question
from klimaat_helpdesk.qa.views import AssignHandlerView
from klimaat_helpdesk.users import HANDLER

User = get_user_model()


class NewQuestions(LoginRequiredMixin, ListView):
    model = TemporaryQuestion
    context_object_name = 'questions'
    template_name = 'moderation/new_questions.html'

    def get_queryset(self):
        qs = super(NewQuestions, self).get_queryset()
        return qs.filter(approved=None)


new_questions_list = NewQuestions.as_view()


class ApproveQuestion(LoginRequiredMixin, View):
    model = TemporaryQuestion
    context_object_name = 'question'
    template_name = 'moderation/approve_question.html'

    def get(self, request, **kwargs):
        question = get_object_or_404(self.model, pk=kwargs['pk'])
        return render(self.request, self.template_name, {self.context_object_name: question})

    def post(self, request, **kwargs):
        temp_question = get_object_or_404(self.model, pk=kwargs['pk'])
        question = temp_question.approve(self.request.user)
        return redirect(reverse_lazy('moderation:assign-hanlder', kwargs={'pk': question.pk}))


approve_question = ApproveQuestion.as_view()


class RejectQuestion(LoginRequiredMixin, UpdateView):
    model = TemporaryQuestion
    context_object_name = 'question'
    template_name = 'moderation/reject_question.html'
    fields = ['rejection', ]
    success_url = reverse_lazy('moderation:new-questions')

    def form_valid(self, form):
        self.object.reject()
        return super(RejectQuestion, self).form_valid(form)


reject_question = RejectQuestion.as_view()


class QuestionAssignHanlder(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['handler', ]
    template_name = 'moderation/assign_handler.html'
    success_url = reverse_lazy('moderation:new-questions')
    context_object_name = 'question'

    def get_form(self, *args, **kwargs):
        form = super(QuestionAssignHanlder, self).get_form(*args, **kwargs)
        form.fields['handler'].queryset = User.objects.filter(role__gte=HANDLER)
        return form

    def form_valid(self, form):
        self.object.date_assigned_handler = now()
        self.object.save()
        return super(QuestionAssignHanlder, self).form_valid(form)


assign_handler = QuestionAssignHanlder.as_view()


class QuestionHandling(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'moderation/handling.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(handler=self.request.user)


question_handling = QuestionHandling.as_view()

