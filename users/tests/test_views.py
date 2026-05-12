from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.models import Position, Team
from work.models import Project


class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Dev")

        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass123",
            position=self.position
        )

        self.client.force_login(self.user)

        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            position=self.position
        )

        self.blank_team, _ = Team.objects.get_or_create(name="Blank")

        self.team = Team.objects.create(name="Team A")

        self.project = Project.objects.create(
            name="Project 1",
            team=self.blank_team
        )

    def test_position_list_view(self):
        url = reverse("users:position-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_worker_list_view(self):
        url = reverse("users:worker-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_worker_detail_view(self):
        url = reverse("users:worker-detail", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_team_list_view(self):
        url = reverse("users:team-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_team_detail_view(self):
        url = reverse("users:team-detail", args=[self.team.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_toggle_assign_to_team(self):
        url = reverse("users:toggle-team-assign", args=[self.team.id])

        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)

    def test_add_project_to_team(self):
        url = reverse("users:team-add-project", args=[self.team.id])

        res = self.client.post(url, {"project_id": self.project.id})
        self.assertEqual(res.status_code, 302)

    def test_remove_project_from_team(self):
        url = reverse(
            "users:team-remove-project",
            args=[self.team.id, self.project.id]
        )

        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
