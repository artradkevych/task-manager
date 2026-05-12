from django.test import TestCase

from work.models import Task, Project
from catalog.models import TaskType, Tag
from users.models import Worker, Team, Position


class WorkModelsTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Dev")

        self.worker = Worker.objects.create_user(
            username="user1",
            password="pass123",
            position=self.position
        )

        self.team = Team.objects.create(name="Team A")

        self.task_type = TaskType.objects.create(name="Bug")
        self.tag = Tag.objects.create(name="Urgent")

        self.project = Project.objects.create(
            name="Project 1",
            team=self.team
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "Project 1")

    def test_task_str(self):
        task = Task.objects.create(
            name="Fix bug",
            description="Bug description",
            deadline="2026-12-31 12:00",
            task_type=self.task_type,
            project=self.project
        )

        task.assignees.add(self.worker)
        task.tags.add(self.tag)

        self.assertIn("Fix bug", str(task))
        self.assertIn("Project 1", str(task))

    def test_task_default_status_and_priority(self):
        task = Task.objects.create(
            name="Task",
            description="Desc",
            deadline="2026-12-31 12:00",
            task_type=self.task_type,
            project=self.project
        )

        self.assertEqual(task.status, "TODO")
        self.assertEqual(task.priority, "MEDIUM")

    def test_project_ordering(self):
        Project.objects.create(name="A Project", team=self.team)
        Project.objects.create(name="B Project", team=self.team)

        projects = Project.objects.all()
        self.assertEqual(projects[0].name, "B Project")
