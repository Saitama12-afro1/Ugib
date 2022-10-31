from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from crud.models import UdsMeta




def validate_pas(value):
    
    if len(value) < 8:
        return ValidationError("Пароль долже содержать больше 7 символов", params={'value':value})
    try:
        val = int(value)
    except ValueError:
        pass
    else:
        return ValidationError("Пароль не должен содержать только цифры")

class UdsMetaForm(forms.ModelForm):
    # stor_folder = forms.CharField(show_hidden_initial=True,initial ="wwwww")
    class Meta:
        model = UdsMeta
        exclude = ('uniq_id', )
  
class WordDocFilling(forms.Form):
    CHOICES = (
        ("выполнение работ по государственным контрактам","выполнение работ по государственным контрактам"),
        ("выполнение работ по государственным заданиям","выполнение работ по государственным заданиям"), 
        ("научные","научные"),
        ("учебные","учебные"),
        ("другое","другое"),
    ) 
    position = forms.CharField(max_length=100)
    departament = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    
    task =  forms.ChoiceField(choices = CHOICES)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_pas])
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    departament = forms.CharField(max_length = 200)
    position = forms.CharField(max_length = 200)
    
    def is_valid(self, password) -> bool:
        super().is_valid()
        value = password
        if len(value) < 8:
                return False
        try:
            val = int(value)
        except ValueError:
            pass
        else:
            return False
        return True
 
    
    
