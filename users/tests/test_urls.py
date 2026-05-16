from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users import views


class UsersUrlsTest(SimpleTestCase):

    def test_position_list_url(self):
        url = reverse("users:position-list")
        self.assertEqual(resolve(url).func.view_class, views.PositionListView)

    def test_position_create_url(self):
        url = reverse("users:position-create")
        self.assertEqual(resolve(url).func.view_class, views.PositionCreateView)

    def test_position_update_url(self):
        url = reverse("users:position-update", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.PositionUpdateView)

    def test_worker_list_url(self):
        url = reverse("users:worker-list")
        self.assertEqual(resolve(url).func.view_class, views.WorkerListView)

    def test_worker_detail_url(self):
        url = reverse("users:worker-detail", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.WorkerDetailView)

    def test_worker_update_url(self):
        url = reverse("users:worker-update", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.WorkerUpdateView)

    def test_worker_create_url(self):
        url = reverse("users:worker-create")
        self.assertEqual(resolve(url).func.view_class, views.WorkerCreateView)

    def test_worker_delete_url(self):
        url = reverse("users:worker-delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.WorkerDeleteView)

    def test_team_list_url(self):
        url = reverse("users:team-list")
        self.assertEqual(resolve(url).func.view_class, views.TeamListView)

    def test_team_detail_url(self):
        url = reverse("users:team-detail", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TeamDetailView)

    def test_team_create_url(self):
        url = reverse("users:team-create")
        self.assertEqual(resolve(url).func.view_class, views.TeamCreateView)

    def test_team_update_url(self):
        url = reverse("users:team-update", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TeamUpdateView)

    def test_team_delete_url(self):
        url = reverse("users:team-delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.TeamDeleteView)

    def test_team_remove_project_url(self):
        url = reverse("users:team-remove-project", args=[1, 2])
        self.assertEqual(resolve(url).func.view_class, views.TeamRemoveProject)

    def test_toggle_team_assign_url(self):
        url = reverse("users:toggle-team-assign", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.ToggleAssignToTeam)

    def test_team_add_project_url(self):
        url = reverse("users:team-add-project", args=[1])
        self.assertEqual(resolve(url).func.view_class, views.AddProjectToTeam)
