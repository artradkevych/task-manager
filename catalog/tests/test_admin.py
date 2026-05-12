from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import TaskType, Tag
from users.models import Position


class CatalogAdminTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Dev")

        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            position=self.position
        )
        self.client.force_login(self.admin)

        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="Backend")

    def test_task_type_list_display(self):
        url = reverse("admin:catalog_tasktype_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.task_type.name)

    def test_tag_list_display(self):
        url = reverse("admin:catalog_tag_changelist")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.tag.name)

    def test_task_type_search(self):
        url = reverse("admin:catalog_tasktype_changelist")
        res = self.client.get(url, {"q": "Bug"})

        self.assertEqual(res.status_code, 200)

    def test_tag_search(self):
        url = reverse("admin:catalog_tag_changelist")
        res = self.client.get(url, {"q": "Backend"})

        self.assertEqual(res.status_code, 200)
