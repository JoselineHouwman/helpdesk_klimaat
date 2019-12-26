from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, FormView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from klimaat_helpdesk.users.forms import CreateUser

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class CreateUserView(FormView):
    form_class = CreateUser
    template_name = 'users/create_user.html'
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.create(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            name=form.cleaned_data['name'],
            role=form.cleaned_data['role']
        )
        user.save()
        return super(CreateUserView, self).form_valid(form)

    def get_success_url(self):
        next = self.request.GET.get('next', None)
        if next:
            return next

        return self.success_url


create_user = CreateUserView.as_view()
