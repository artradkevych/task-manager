from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from work.models import Task, Project
from catalog.models import TaskType
from users.models import Position, Worker, Team


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Dev")

        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            position=self.position
        )
        self.client.force_login(self.admin)

        self.worker = Worker.objects.create_user(
            username="worker1",
            password="pass123",
            position=self.position
        )

        self.team = Team.objects.create(name="Team A")

        self.task_type = TaskType.objects.create(name="Bug")

        self.project = Project.objects.create(
            name="Project 1",
            team=self.team
        )

        self.task = Task.objects.create(
            name="Task 1",
            description="Desc",
            deadline="2026-12-31 12:00",
            task_type=self.task_type,
            project=self.project
        )
        self.task.assignees.add(self.worker)

    def test_task_list_display(self):
        url = reverse("admin:work_task_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.task.name)
        self.assertContains(res, self.worker.username)
        self.assertContains(res, self.project.name)

    def test_task_search_fields(self):
        url = reverse("admin:work_task_changelist")
        res = self.client.get(url, {"q": "Task"})

        self.assertEqual(res.status_code, 200)

    def test_project_list_display(self):
        url = reverse("admin:work_project_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.project.name)
        self.assertContains(res, self.team.name)
