from django.test import TestCase

from users.admin import WorkerAdmin, PositionAdmin, TeamAdmin


class AdminTest(TestCase):

    def test_worker_admin_config(self):
        self.assertIn("position", WorkerAdmin.list_display)
        self.assertIn("position", WorkerAdmin.list_filter)

        fieldsets = WorkerAdmin.fieldsets
        self.assertTrue(
            any("position" in str(fs) for fs in fieldsets)
        )

        add_fieldsets = WorkerAdmin.add_fieldsets
        self.assertTrue(
            any("position" in str(fs) for fs in add_fieldsets)
        )

    def test_position_admin_config(self):
        self.assertEqual(PositionAdmin.list_display, ("name",))
        self.assertEqual(PositionAdmin.search_fields, ("name",))

    def test_team_admin_config(self):
        self.assertIn("name", TeamAdmin.list_display)
        self.assertIn("created_at", TeamAdmin.list_display)
        self.assertIn("workers_count", TeamAdmin.list_display)

        self.assertEqual(TeamAdmin.search_fields, ("name",))
