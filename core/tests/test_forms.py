from django.test import TestCase
from core.forms import BaseSearchForm, BaseNameSearchForm


class BaseSearchFormTest(TestCase):
    def test_base_search_form_has_query_field(self):
        form = BaseSearchForm()

        self.assertIn("query", form.fields)
        self.assertEqual(form.fields["query"].required, False)
        self.assertEqual(form.fields["query"].label, "")

    def test_base_search_form_widget_attributes(self):
        form = BaseSearchForm()

        widget = form.fields["query"].widget
        self.assertEqual(widget.attrs["class"], "form-control")
        self.assertEqual(widget.attrs["placeholder"], "Search by name")

    def test_base_search_form_valid_data(self):
        form = BaseSearchForm(data={"query": "test"})
        self.assertTrue(form.is_valid())

    def test_base_search_form_empty_valid(self):
        form = BaseSearchForm(data={})
        self.assertTrue(form.is_valid())


class BaseNameSearchFormTest(TestCase):
    def test_inherits_from_base_search_form(self):
        form = BaseNameSearchForm()

        self.assertIn("query", form.fields)
        self.assertEqual(form.fields["query"].widget.attrs["placeholder"], "Search by name")
