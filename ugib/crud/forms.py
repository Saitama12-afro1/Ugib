from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from crud.models import UdsMeta, UdsMetaApr




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
class UdsMetaAprForm(forms.ModelForm):
    
    class Meta:
        model = UdsMetaApr
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
    username = forms.CharField(label='Почта',max_length=100)
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Почта',max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_pas])
    first_name = forms.CharField(label='Имя Отчество', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    departament = forms.CharField(label='Отдел',max_length = 200)
    position = forms.CharField(label='Должность',max_length = 200)
    
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

class MyChangePassword(forms.Form):
    mail = forms.EmailField(label="Введите вашу почту")
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Потоврите пароль', widget=forms.PasswordInput)
    
    error_messages = {
        "password_mismatch": ("Пароли не совпадают"),
        "pass_no_len" : ("Пароль слишком мал"),
        "pass_zero_letter" :("Пароль не должен содержать одни цифры"),
        "invalid_mail" : ("Введите вашу почту"),
    }
    def test_pas(self) -> bool:
       
        if self.cleaned_data.get("password")!= self.cleaned_data.get("repeat_password"):
            raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        if len(self.cleaned_data.get("password")) < 7:
             raise ValidationError(
                    self.error_messages["pass_no_len"],
                    code="pass_no_len",
                )
        try: 
            int(self.cleaned_data.get("password"))
            raise ValidationError(
                    self.error_messages["pass_zero_letter"],
                    code="pass_zero_letter",
                )
        except ValueError:
            pass
        return super().is_valid()
    
    def test_mail(self, all_mails):
        if self.cleaned_data.get("mail") not in all_mails:
             raise ValidationError(
                    self.error_messages["invalid_mail"],
                    code="invalid_mail",
                ) 
    
    def get_current_user(self, user):
        self.user = user
        return self.user

    
    field_order = ["mail", "password", "repeat_password"]


