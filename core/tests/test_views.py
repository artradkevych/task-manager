from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.models import Position, Team
from work.models import Task, Project
from catalog.models import TaskType


class CoreViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Dev")

        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass123",
            position=self.position
        )

        self.client.force_login(self.user)

        self.team = Team.objects.create(name="Team A")

        self.project = Project.objects.create(
            name="Project 1",
            team=self.team
        )

        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Task 1",
            description="Test",
            deadline="2030-01-01 00:00:00",
            task_type=self.task_type,
            project=self.project,
            status="TODO",
            priority="MEDIUM",
        )

        self.task.assignees.add(self.user)

    def test_index_view_status_code(self):
        url = reverse("index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_index_view_context_counts(self):
        url = reverse("index")
        res = self.client.get(url)

        self.assertEqual(res.context["tasks_count"], 1)
        self.assertEqual(res.context["projects_count"], 1)
        self.assertEqual(res.context["teams_count"], 1)
        self.assertEqual(res.context["workers_count"], 1)

    def test_index_view_tasks_filtering(self):
        url = reverse("index")
        res = self.client.get(url)

        self.assertEqual(len(res.context["latest_tasks"]), 1)
        self.assertEqual(len(res.context["completed_tasks"]), 0)

    def test_index_view_session_counter(self):
        url = reverse("index")

        self.client.get(url)
        self.client.get(url)
        res = self.client.get(url)

        self.assertEqual(res.context["num_visits"], 3)
