from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import Tag, TaskType
from users.models import Position


class CatalogViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.position = Position.objects.create(name="Dev")

        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass123",
            position=self.position
        )
        self.client.force_login(self.user)

        self.tag = Tag.objects.create(name="Backend")
        self.task_type = TaskType.objects.create(name="Bug")

    def test_tag_list_view(self):
        url = reverse("catalog:tag-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.tag.name)

    def test_tag_create_view(self):
        url = reverse("catalog:tag-create")

        res = self.client.post(url, {"name": "Frontend"})

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="Frontend").exists())

    def test_tag_update_view(self):
        url = reverse("catalog:tag-update", args=[self.tag.id])

        res = self.client.post(url, {"name": "Updated"})

        self.assertEqual(res.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated")

    def test_tag_delete_view(self):
        url = reverse("catalog:tag-delete", args=[self.tag.id])

        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())

    def test_task_type_list_view(self):
        url = reverse("catalog:task_type-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.task_type.name)

    def test_task_type_create_view(self):
        url = reverse("catalog:task_type-create")

        res = self.client.post(url, {"name": "Feature"})

        self.assertEqual(res.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Feature").exists())

    def test_task_type_update_view(self):
        url = reverse("catalog:task_type-update", args=[self.task_type.id])

        res = self.client.post(url, {"name": "Improvement"})

        self.assertEqual(res.status_code, 302)
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Improvement")
