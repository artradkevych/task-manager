from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.models import Position, Team
from work.models import Project, TaskType, Task


class WorkUrlsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")

        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass123",
            position=self.position
        )

        self.client.force_login(self.user)

        self.team = Team.objects.create(name="Team")
        self.blank_team, _ = Team.objects.get_or_create(name="Blank")

        self.project = Project.objects.create(
            name="Project",
            team=self.blank_team
        )

        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Task",
            description="Desc",
            deadline="2030-01-01T00:00",
            task_type=self.task_type,
            project=self.project
        )

    def test_task_list_url(self):
        url = reverse("work:task-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_task_detail_url(self):
        url = reverse("work:task-detail", args=[self.task.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_task_create_url(self):
        url = reverse("work:task-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_task_update_url(self):
        url = reverse("work:task-update", args=[self.task.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_task_delete_url(self):
        url = reverse("work:task-delete", args=[self.task.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_send_to_review_url(self):
        url = reverse("work:send_to_review", args=[self.task.id])
        res = self.client.post(url)
        self.assertIn(res.status_code, (302, 403))

    def test_approve_url(self):
        url = reverse("work:approve", args=[self.task.id])
        res = self.client.post(url)
        self.assertIn(res.status_code, (302, 403))

    def test_add_assignee_url(self):
        url = reverse("work:add-assignee", args=[self.task.id])
        res = self.client.post(url, {"worker_id": self.user.id})
        self.assertEqual(res.status_code, 302)

    def test_remove_assignee_url(self):
        url = reverse(
            "work:remove-assignee",
            args=[self.task.id, self.user.id]
        )
        res = self.client.post(url)
        self.assertIn(res.status_code, (302, 403))

    def test_project_list_url(self):
        url = reverse("work:project-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_project_detail_url(self):
        url = reverse("work:project-detail", args=[self.project.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_project_create_url(self):
        url = reverse("work:project-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_project_update_url(self):
        url = reverse("work:project-update", args=[self.project.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_project_delete_url(self):
        url = reverse("work:project-delete", args=[self.project.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_project_add_task_url(self):
        url = reverse("work:project-add-task", args=[self.project.id])
        res = self.client.post(url, {"task_id": self.task.id})
        self.assertEqual(res.status_code, 302)

    def test_project_remove_task_url(self):
        url = reverse(
            "work:project-remove-task",
            args=[self.project.id, self.task.id]
        )
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
