from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

VALIDATE_ONLY_LETTERS_EXCEPTION_MESSAGE = 'Ensure this field contains only letters.'


def only_letters_validator(value):
    if not value.isalpha():
        raise ValidationError(VALIDATE_ONLY_LETTERS_EXCEPTION_MESSAGE)


@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(self.__get_exception_message())

    def __get_exception_message(self):
        return f'Value must be greater than {self.min_date}'
