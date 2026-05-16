from django.test import TestCase
from django.contrib.auth import get_user_model

from work.forms import TaskForm, TaskSearchForm, ProjectSearchForm
from work.models import Tag, TaskType, Project
from users.models import Team, Position


class TaskFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")

        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass123",
            position=self.position
        )

        self.team = Team.objects.create(name="Team")
        self.project = Project.objects.create(
            name="Project",
            team=self.team
        )

        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="Urgent")

    def test_task_form_valid(self):
        form_data = {
            "name": "Task 1",
            "description": "Desc",
            "deadline": "2030-01-01T10:00",
            "status": "TODO",
            "priority": "MEDIUM",
            "task_type": self.task_type.id,
            "project": self.project.id,
            "assignees": [self.user.id],
            "tags": [self.tag.id],
        }

        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_required_fields(self):
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())


class TaskSearchFormTest(TestCase):
    def test_task_search_form_valid(self):
        form = TaskSearchForm(data={"query": "test"})
        self.assertTrue(form.is_valid())

    def test_task_search_form_empty_valid(self):
        form = TaskSearchForm(data={"query": ""})
        self.assertTrue(form.is_valid())


class ProjectSearchFormTest(TestCase):
    def test_project_search_form_valid(self):
        form = ProjectSearchForm(data={"query": "test"})
        self.assertTrue(form.is_valid())
