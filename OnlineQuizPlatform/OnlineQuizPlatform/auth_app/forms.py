from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from OnlineQuizPlatform.auth_app.models import Profile, QuizUser
from OnlineQuizPlatform.common.helpers import BootstrapFormMixin


class UserLoginForm(BootstrapFormMixin, auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_control()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserRegistrationForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=Profile.FIRST_NAME_MAX_LEN,)
    last_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LEN,)
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=Profile.GENDERS,)
    city = forms.CharField(max_length=Profile.CITY_MAX_LEN,)
    picture = forms.URLField()
    description = forms.CharField(widget=forms.Textarea,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_control()

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            city=self.cleaned_data['city'],
            picture=self.cleaned_data['picture'],
            description=self.cleaned_data['description'],
            user=user,
        )

        if commit:
            profile.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'gender', 'city', 'picture', 'description')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=QuizUser.USERNAME_MAX_LEN, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=Profile.FIRST_NAME_MAX_LEN, widget=forms.TextInput())
    last_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LEN, widget=forms.TextInput())
    date_of_birth = forms.DateField(widget=forms.DateInput,)
    city = forms.CharField(max_length=Profile.CITY_MAX_LEN, widget=forms.TextInput)
    picture = forms.URLField(widget=forms.URLInput)
    description = forms.CharField(widget=forms.Textarea, )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'city', 'picture', 'description')


class DeleteUserForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = get_user_model()
        fields = ()

