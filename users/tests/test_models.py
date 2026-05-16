from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Position, Team

Worker = get_user_model()


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")

        cls.worker = Worker.objects.create_user(
            username="test_user",
            password="test123",
            first_name="Test",
            last_name="User",
            position=cls.position
        )

        cls.team = Team.objects.create(
            name="Backend",
            description="Backend team"
        )
        cls.team.workers.add(cls.worker)

    def test_position_str(self):
        self.assertEqual(str(self.position), self.position.name)

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.first_name} "
            f"{self.worker.last_name} "
            f"({self.position})"
        )

    def test_team_str(self):
        self.assertEqual(str(self.team), self.team.name)

    def test_team_workers_count(self):
        self.assertEqual(self.team.workers_count, 1)
