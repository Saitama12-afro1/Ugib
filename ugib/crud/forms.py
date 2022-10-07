from turtle import position
from django import forms


from crud.models import UdsMeta

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