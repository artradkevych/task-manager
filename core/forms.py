from django import forms


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