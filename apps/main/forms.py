from django import forms

# class KeyForm(forms.Form):
#     key = forms.CharField(label='Key', max_length=200)
from django.forms import Textarea

from .models import UserProfile


class VerifyUlxKey(forms.Form):
    # Just some simple form to grab a value, and return it to us. ( I think we can still load something into here with
    # The Lua side? Looks like if we post, it gets into the request dict still that way, so now we just throw it in here
    # somehow?
    key_value = forms.CharField(max_length=200)


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('bio', 'signature', 'motto')
        widgets = {
            'bio': Textarea(attrs={'cols': 100, 'rows': 20}),
            'signature': Textarea(attrs={'cols': 100, 'rows': 10}),
            'motto': Textarea(attrs={'cols': 100, 'rows': 5}),
        }
