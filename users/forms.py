from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from work.forms import BaseSearchForm
from users.models import Worker, Team


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


class WorkerSearchForm(BaseSearchForm):
    placeholder = "Search by username, email or name"


class TeamSearchForm(BaseSearchForm):
    placeholder = "Search by name, description or members"
