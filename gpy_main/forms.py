from django import forms


# class KeyForm(forms.Form):
#     key = forms.CharField(label='Key', max_length=200)
from .models import GpyProfile


class GpyProfileForm(forms.ModelForm):
    class Meta():
        model = GpyProfile
        fields = ('bio', 'signature', 'motto')
    # bio = forms.CharField(label='Biography', max_length=600)
    # signature = forms.CharField(label='Forum Signature', max_length=200)
    # motto = forms.CharField(label='Motto', max_length=100)

