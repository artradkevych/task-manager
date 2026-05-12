from django.test import TestCase
from catalog.models import TaskType, Tag


class TaskTypeModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug")

    def test_task_type_ordering(self):
        TaskType.objects.create(name="Alpha")
        TaskType.objects.create(name="Zeta")

        names = list(TaskType.objects.values_list("name", flat=True))
        self.assertEqual(names, sorted(names))


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Backend")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Backend")

    def test_tag_ordering(self):
        Tag.objects.create(name="API")
        Tag.objects.create(name="UI")

        names = list(Tag.objects.values_list("name", flat=True))
        self.assertEqual(names, sorted(names))
