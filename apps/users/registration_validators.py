import re
from rest_framework import exceptions
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext as _


def validate_number(number):
    char = re.findall(r'(?:[a-zA-Z])', number.lower())
    if len(char) != 0:
        raise exceptions.ValidationError('Number is not valid',
                                         code='Number should contain only digits')
    if not re.findall(r"(?:[0-9]{9})", number):
        raise exceptions.ValidationError('Number is not valid',
                                         code='Numbers length is should be 9')


class UppercaseValidator(object):
    '''The password must contain at least 1 uppercase letter, A-Z.'''

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class IsIncludeOneDigit(object):
    def validate(self, password, user=None):
        if not re.findall(r'(?:[0-9])', password):
            raise ValidationError(_(f'Password must include at least one digit'),
                                  code=f'password_no_digit', )

    def get_help_text(self):
        return _('Password must include at least one digit')


class IsIncludeOnlyLatyn(object):
    def validate(self, password, user=None):
        if re.findall(r"(?:[а-яА-ЯёЁ])", password):
            raise ValidationError(_('Password must include only latn letters'),
                                  code='password should contain only latn letters')

    def get_help_text(self):
        return _('Password must include only latyn letters')