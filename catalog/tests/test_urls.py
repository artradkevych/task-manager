from django.test import TestCase
from django.urls import reverse

from catalog.models import Tag, TaskType


class CatalogUrlsTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name="Backend")
        self.task_type = TaskType.objects.create(name="Bug")

    def test_tag_list_url(self):
        res = self.client.get(reverse("catalog:tag-list"))
        self.assertEqual(res.status_code, 302)

    def test_tag_create_url(self):
        res = self.client.get(reverse("catalog:tag-create"))
        self.assertEqual(res.status_code, 302)

    def test_tag_update_url(self):
        res = self.client.get(reverse("catalog:tag-update", args=[self.tag.id]))
        self.assertEqual(res.status_code, 302)

    def test_tag_delete_url(self):
        res = self.client.get(reverse("catalog:tag-delete", args=[self.tag.id]))
        self.assertEqual(res.status_code, 302)

    def test_task_type_list_url(self):
        res = self.client.get(reverse("catalog:task_type-list"))
        self.assertEqual(res.status_code, 302)

    def test_task_type_create_url(self):
        res = self.client.get(reverse("catalog:task_type-create"))
        self.assertEqual(res.status_code, 302)

    def test_task_type_update_url(self):
        res = self.client.get(reverse("catalog:task_type-update", args=[self.task_type.id]))
        self.assertEqual(res.status_code, 302)
