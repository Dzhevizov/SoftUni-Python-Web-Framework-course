from django.contrib import messages
from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.auth_app.forms import UserRegistrationForm, UserLoginForm, EditProfileForm, EditUserForm, \
    DeleteUserForm
from OnlineQuizPlatform.auth_app.models import Profile


class UserLoginView(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'auth_user/login.html'

    def get_success_url(self):
        _next = self.request.GET.get('next', None)
        if _next:
            return _next
        return reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):
    next_page = 'index'


class RestrictedView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = 'index.html'


class UserRegisterView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'auth_user/register.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'auth_user/profile_details.html'
    context_object_name = 'profile'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #
    #
    #     context.update({
    #
    #     })
    #
    #     return context


@login_required
def edit_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile', pk=pk)
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=profile)

    return render(request, 'auth_user/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class DeleteProfileView(views.DeleteView):
    model = get_user_model()
    form_class = DeleteUserForm
    template_name = 'auth_user/delete_profile.html'
    success_url = reverse_lazy('index')


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'auth_user/change_password.html'
