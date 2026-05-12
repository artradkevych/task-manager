from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tasks.models import Task, Tag, Worker, Team


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


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerUpdateForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        )


class TeamForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Team
        fields = "__all__"


class BaseSearchForm(forms.Form):
    field_name = "query"
    placeholder = "Search by name"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.field_name] = forms.CharField(
            max_length=255,
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": self.placeholder,
                }
            )
        )


class BaseNameSearchForm(BaseSearchForm):
    pass


class TaskSearchForm(BaseSearchForm):
    placeholder = "Search by name, description or tag"


class ProjectSearchForm(BaseSearchForm):
    placeholder = "Search by name, description or tasks"


class WorkerSearchForm(BaseSearchForm):
    placeholder = "Search by username, email or name"


class TeamSearchForm(BaseSearchForm):
    placeholder = "Search by name, description or members"
