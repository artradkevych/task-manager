from django.test import TestCase
from django.contrib.auth import get_user_model

from users.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    TeamForm,
    WorkerSearchForm,
    TeamSearchForm
)
from users.models import Position, Team


class WorkerFormsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")

    def test_worker_creation_form_valid(self):
        form_data = {
            "username": "user1",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "position": self.position.id
        }

        form = WorkerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_worker_update_form_valid(self):
        user = get_user_model().objects.create_user(
            username="user1",
            password="pass123",
            position=self.position
        )

        form_data = {
            "username": "user1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "position": self.position.id
        }

        form = WorkerUpdateForm(instance=user, data=form_data)

        self.assertTrue(form.is_valid())


class TeamFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")

        self.worker = get_user_model().objects.create_user(
            username="worker1",
            password="pass123",
            position=self.position
        )

    def test_team_form_valid(self):
        form_data = {
            "name": "Team A",
            "description": "Test team",
            "workers": [self.worker.id]
        }

        form = TeamForm(data=form_data)

        self.assertTrue(form.is_valid())


class SearchFormsTest(TestCase):
    def test_worker_search_form(self):
        form = WorkerSearchForm(data={"query": "john"})
        self.assertTrue(form.is_valid())

    def test_team_search_form(self):
        form = TeamSearchForm(data={"query": "dev"})
        self.assertTrue(form.is_valid())
