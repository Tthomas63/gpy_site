from django import forms


# class KeyForm(forms.Form):
#     key = forms.CharField(label='Key', max_length=200)
from django.forms import Textarea

from .models import GpyProfile


class GpyProfileForm(forms.ModelForm):
    class Meta():
        model = GpyProfile
        fields = ('bio', 'signature', 'motto')
        widgets = {
            'bio': Textarea(attrs={'cols': 100, 'rows': 20}),
            'signature': Textarea(attrs={'cols': 100, 'rows': 10}),
            'motto': Textarea(attrs={'cols': 100, 'rows': 5}),
        }

