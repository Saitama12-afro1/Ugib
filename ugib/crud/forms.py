from django import forms


from crud.models import UdsMeta

class UdsMetaForm(forms.ModelForm):
    # stor_folder = forms.CharField(show_hidden_initial=True,initial ="wwwww")
    class Meta:
        model = UdsMeta
        exclude = ("oid", "uniq_id")
  

    