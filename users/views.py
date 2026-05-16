from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from core.views import BaseSearchListView
from work.models import Task, Project
from users.forms import (
    TeamSearchForm,
    WorkerUpdateForm,
    WorkerCreationForm,
    WorkerSearchForm,
    TeamForm
)
from users.models import Position, Worker, Team


class PositionListView(BaseSearchListView):
    model = Position
    context_object_name = "position_list"
    paginate_by = 30
    search_fields = ["name"]


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("users:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("users:position-list")


class WorkerListView(BaseSearchListView):
    model = Worker
    context_object_name = "worker_list"
    paginate_by = 6
    search_form_class = WorkerSearchForm
    search_fields = ["username", "first_name", "last_name", "email"]


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["active_tasks"] = Task.objects.filter(
            assignees=self.object,
            status__in=("TODO", "IN_PROGRESS")
        )
        context["completed_tasks"] = Task.objects.filter(
            assignees=self.object,
            status__in=("DONE", "IN_REVIEW")
        )
        context["teams"] = Team.objects.all()

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("users:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "users:worker-detail",
            kwargs={"pk": self.object.pk}
        )


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("users:worker-list")


class TeamListView(BaseSearchListView):
    model = Team
    context_object_name = "team_list"
    paginate_by = 9
    search_form_class = TeamSearchForm
    search_fields = ["name", "description", "workers__username"]


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blank_team, _ = Team.objects.get_or_create(
            name="Blank",
        )
        context["available_projects"] = Project.objects.filter(
            team=blank_team
        )

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("users:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("users:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("users:team-list")


class ToggleAssignToTeam(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        worker = request.user
        if worker.teams.filter(pk=pk).exists():
            worker.teams.remove(pk)
        else:
            worker.teams.add(pk)
        return redirect("users:team-detail", pk=pk)


class TeamRemoveProject(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int, project_id: int):
        project = get_object_or_404(Project, pk=project_id)

        blank_team, _ = Team.objects.get_or_create(
            name="Blank",
        )
        project.team = blank_team
        project.save()

        return redirect("users:team-detail", pk=pk)


class AddProjectToTeam(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        team = get_object_or_404(Team, pk=pk)
        project_id = request.POST.get("project_id")

        if project_id:
                project = get_object_or_404(Project, pk=project_id)
                project.team = team
                project.save()

        return redirect("users:team-detail", pk=pk)
