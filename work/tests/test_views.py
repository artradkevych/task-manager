from django.test import TestCase, Client
from django.urls import reverse

from work.models import Task, Project, TaskType
from users.models import Worker, Position, Team


class WorkViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Dev")

        self.user = Worker.objects.create_user(
            username="user",
            password="testpass123",
            position=self.position
        )

        self.admin = Worker.objects.create_superuser(
            username="admin",
            password="admin123",
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
            description="desc",
            deadline="2030-01-01T00:00:00",
            task_type=self.task_type,
            project=self.project
        )

    def test_send_task_to_review(self):
        self.task.assignees.add(self.user)

        url = reverse("work:send_to_review", args=[self.task.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)

    def test_approve_task_as_admin(self):
        self.task.status = "IN_REVIEW"
        self.task.save()

        self.client.force_login(self.admin)

        url = reverse("work:approve", args=[self.task.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)

    def test_add_task_to_project(self):
        url = reverse("work:project-add-task", args=[self.project.id])

        res = self.client.post(url, {
            "task_id": self.task.id
        })

        self.assertEqual(res.status_code, 302)

    def test_remove_task_from_project(self):
        url = reverse("work:project-remove-task", args=[self.project.id, self.task.id])

        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)

    def test_add_assignee(self):
        url = reverse("work:add-assignee", args=[self.task.id])

        res = self.client.post(url, {
            "worker_id": self.user.id
        })

        self.assertEqual(res.status_code, 302)

    def test_remove_assignee(self):
        self.task.assignees.add(self.user)

        self.client.force_login(self.admin)

        url = reverse("work:remove-assignee", args=[self.task.id, self.user.id])

        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
