from django import forms
# class KeyForm(forms.Form):
#     key = forms.CharField(label='Key', max_length=200)
from django.forms import Textarea


class RconCmdForm(forms.Form):
    rcon_server_port = forms.CharField(label='Rcon Server', max_length=100)
    rcon_cmd = forms.CharField(label='Rcon Command', max_length=100)
