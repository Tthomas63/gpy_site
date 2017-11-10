from django.forms import ModelForm

from .models import Forum


class PartialForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = '__all__'