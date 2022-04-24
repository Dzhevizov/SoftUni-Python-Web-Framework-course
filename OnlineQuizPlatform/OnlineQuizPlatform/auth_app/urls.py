from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from OnlineQuizPlatform.auth_app.views import UserLoginView, UserLogoutView, RestrictedView, UserRegisterView, \
    ProfileDetailsView, edit_profile, DeleteProfileView, ChangeUserPasswordView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('restricted/', RestrictedView.as_view(), name='restricted'),
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', edit_profile, name='edit profile'),
    path('profile/delete/<int:pk>', DeleteProfileView.as_view(), name='delete profile'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('index')), name='password_change_done'),
)
