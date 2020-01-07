from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, UpdateView, CreateView, FormView
from django.views.generic.base import View
from django.utils.translation import gettext as _

from klimaat_helpdesk.moderation.forms import ExpertCreationForm
from klimaat_helpdesk.qa import ANSWERING
from klimaat_helpdesk.qa.models import TemporaryQuestion, Question
from klimaat_helpdesk.users import HANDLER, EXPERT
from klimaat_helpdesk.users.models import ExpertProfile

User = get_user_model()


class NewQuestions(LoginRequiredMixin, ListView):
    """List of questions in need of a decision. Either approve or reject.
    """
    model = TemporaryQuestion
    context_object_name = 'questions'
    template_name = 'moderation/new_questions.html'

    def get_queryset(self):
        qs = super(NewQuestions, self).get_queryset()
        return qs.filter(approved=None)


new_questions_list = NewQuestions.as_view()


class ApproveQuestion(LoginRequiredMixin, View):
    """A bit more convoluted than needed. To keep the principle that only a post request can be used to update/create an
    object."""
    model = TemporaryQuestion
    context_object_name = 'question'
    template_name = 'moderation/approve_question.html'

    def get(self, request, **kwargs):
        question = get_object_or_404(self.model, pk=kwargs['pk'])
        return render(self.request, self.template_name, {self.context_object_name: question})

    def post(self, request, **kwargs):
        temp_question = get_object_or_404(self.model, pk=kwargs['pk'])
        question = temp_question.approve(self.request.user)
        return redirect(reverse_lazy('moderation:assign-handler', kwargs={'pk': question.pk}))


approve_question = ApproveQuestion.as_view()


class RejectQuestion(LoginRequiredMixin, UpdateView):
    """When rejecting a question, a reason must be provided. This is useful for bookkeeping and to inform the user who
    asked."""

    model = TemporaryQuestion
    context_object_name = 'question'
    template_name = 'moderation/reject_question.html'
    fields = ['rejection', ]
    success_url = reverse_lazy('moderation:new-questions')

    def form_valid(self, form):
        self.object.reject()
        return super(RejectQuestion, self).form_valid(form)


reject_question = RejectQuestion.as_view()


class QuestionAssignHandler(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['handler', ]
    template_name = 'moderation/assign_handler.html'
    success_url = reverse_lazy('moderation:new-questions')
    context_object_name = 'question'

    def get_form(self, *args, **kwargs):
        form = super(QuestionAssignHandler, self).get_form(*args, **kwargs)
        form.fields['handler'].queryset = User.objects.filter(role__gte=HANDLER)
        return form

    def form_valid(self, form):
        self.object.date_assigned_handler = now()
        self.object.save()
        return super(QuestionAssignHandler, self).form_valid(form)


assign_handler = QuestionAssignHandler.as_view()


class QuestionHandling(LoginRequiredMixin, ListView):
    """List the questions the logged-in user has to handle.
    """
    model = Question
    context_object_name = 'questions'
    template_name = 'moderation/handling.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(handler=self.request.user)


question_handling = QuestionHandling.as_view()


class AssignExpert(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    fields = ['expert', ]
    context_object_name = 'question'
    template_name = 'moderation/assign_expert.html'
    success_message = "Expert added successfully"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().handler != self.request.user:
            return HttpResponseForbidden()
        return super(AssignExpert, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super(AssignExpert, self).get_form(*args, **kwargs)
        form.fields['expert'].queryset = User.objects.filter(role__gte=EXPERT)
        return form

    def get_success_url(self):
        return reverse_lazy('moderation:assign-expert', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object.date_assigned_expert = now()
        self.object.status = ANSWERING
        self.object.save()
        return super(AssignExpert, self).form_valid(form)


assign_expert = AssignExpert.as_view()


class CreateExpert(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ExpertCreationForm
    template_name = 'moderation/create_expert.html'
    extra_context = {'title': _('Update Expert Profile')}
    success_message = _('Expert created successfully')

    def form_valid(self, form):
        self.object = form.save()
        return super(CreateExpert, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('moderation:create-expert-profile', kwargs={'pk': self.object.expert_profile.pk})


create_expert = CreateExpert.as_view()


class CreateExpertProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ExpertProfile
    fields = ['bio',
              'profile_picture',
              'areas_expertise',
              'affiliation',
              'website',
              'twitter_profile',
              'linkedin_profile',
              ]
    template_name = 'moderation/create_expert_profile.html'
    success_message = _('Expert profile created successfully')
    success_url = reverse_lazy('moderation:handling')
    context_object_name = 'profile'


create_expert_profile = CreateExpertProfile.as_view()
