from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ValidPas:
    def validate(*args):
        print(args)
        value = args[1]
        if len(value) < 8:
            raise ValidationError("Пароль должен содержать больше 7 символов", params={'value':value})
        try:
            val = int(value)
        except ValueError:
            raise ValidationError("Пароль не должен содержать только цифры")
        else:
            raise ValidationError("Пароль не должен содержать только цифры")

    def get_help_text(self):
            return _(
                "Пароль не должен содержать только цифры и должен содержать больше 7 символов",
            )