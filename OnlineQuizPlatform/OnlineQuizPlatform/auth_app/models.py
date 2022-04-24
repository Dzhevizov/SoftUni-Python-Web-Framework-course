import datetime

from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db import models

from OnlineQuizPlatform.auth_app.managers import QuizUserManager
from OnlineQuizPlatform.common.validators import only_letters_validator, MinDateValidator


class QuizUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LEN = 20
    USERNAME_MIN_LEN = 5

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        unique=True,
        validators=(
            MinLengthValidator(USERNAME_MIN_LEN),
        )
    )

    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = QuizUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    FIRST_NAME_MAX_LEN = 20
    FIRST_NAME_MIN_LEN = 2

    LAST_NAME_MAX_LEN = 20
    LAST_NAME_MIN_LEN = 2

    DATE_OF_BIRTH_MIN_DATE = datetime.date(1920, 1, 1)

    MALE = 'Male'
    FEMALE = 'Female'

    GENDERS = [(x, x) for x in (MALE, FEMALE)]

    CITY_MAX_LEN = 25
    CITY_MIN_LEN = 3

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            only_letters_validator,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
            only_letters_validator,
        )
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=(
            MinDateValidator(DATE_OF_BIRTH_MIN_DATE),
        )
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=CITY_MAX_LEN,
        null=True,
        blank=True,
        validators=(
            MinLengthValidator(CITY_MIN_LEN),
        )
    )

    picture = models.URLField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        QuizUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
