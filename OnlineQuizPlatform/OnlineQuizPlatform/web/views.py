from django import forms
from django.contrib.auth import views as auth_views, login
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import forms as auth_forms


class UserRegistrationForm(auth_forms.UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=commit)

        # profile = Profile(
        #     first_name=self.cleaned_data['first_name'],
        #     user=user,
        # )

        # if commit:
        #     profile.save()

        return user


class UserRegistrationView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('index')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['profile_form'] = ProfileCreateForm()
    #     return context

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'auth/login.html'

    def get_success_url(self):
        next = self.request.GET.get('next', None)
        if next:
            return next
        return reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):

    pass
