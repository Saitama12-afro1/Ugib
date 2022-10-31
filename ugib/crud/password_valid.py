from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ValidPas:
    def validate(value):
        if len(value) < 8:
            return ValidationError("Пароль должен содержать больше 7 символов", params={'value':value})
        try:
            val = int(value)
        except ValueError:
            pass
        else:
            return ValidationError("Пароль не должен содержать только цифры")
        
    def get_help_text(self):
            return _(
                "Пароль не должен содержать только цифры и должен содержать больше 7 символов",
            )