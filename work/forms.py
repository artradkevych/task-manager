from django import forms
from django.contrib.auth import get_user_model

from core.forms import BaseSearchForm
from work.models import Task, Tag


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            )
        }


class TaskSearchForm(BaseSearchForm):
    placeholder = "Search by name, description or tag"


class ProjectSearchForm(BaseSearchForm):
    placeholder = "Search by name, description or work"
