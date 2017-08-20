from django import forms
# class KeyForm(forms.Form):
#     key = forms.CharField(label='Key', max_length=200)
from django.forms import Textarea

SERVER_CHOICES = (
    ('27015', 'TTT'),
    ('27016', 'DarkRP'),
)

class RconCmdForm(forms.Form):
    rcon_server_port = forms.CharField(label='Rcon Server', max_length=100)
    rcon_cmd = forms.CharField(label='Rcon Command', max_length=100)


class BanUserForm(forms.Form):
    rcon_server_port = forms.ChoiceField(label='Rcon Server', choices=SERVER_CHOICES)
    steam_id = forms.CharField(label='SteamID for user', max_length=20)
    duration = forms.CharField(label="Duration in mins. 0 is permanent.", max_length=5)
    reason = forms.CharField(label="Reason for ban", max_length=50, widget=forms.Textarea)
    # steam_id_registered_user = forms.CharField(label="Registed site user", max_length=20)