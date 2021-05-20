from django import forms
from django.forms.utils import ErrorList

from health_tracker.models import Value


class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        fields = ['date','value','user']

    def save(self, commit=True):
        self.instance.user=self.user
        return super().save(commit)



