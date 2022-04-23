from django.urls import path
from django.views.generic import TemplateView

from OnlineQuizPlatform.web.views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = (
    path('auth/register/', UserRegistrationView.as_view(), name='register user'),
    path('auth/login/', UserLoginView.as_view(), name='login user'),
    path('auth/logout/', UserLogoutView.as_view(), name='logout user'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
)
