from django import forms


class KeyForm(forms.Form):
    key = forms.CharField(label='Key', max_length=200)
