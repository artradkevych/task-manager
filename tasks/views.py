from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import (
    TaskForm,
    WorkerCreationForm,
    TeamForm,
    BaseNameSearchForm,
    WorkerUpdateForm,
    TaskSearchForm,
    ProjectSearchForm,
    WorkerSearchForm,
    TeamSearchForm,
)
from tasks.models import (
    Task,
    Team,
    Worker,
    Tag,
    TaskType,
    Project,
    Position,
)


@login_required
def index(request):
    """View function for the home page of the site."""

    tasks_count = Task.objects.count()
    projects_count = Project.objects.count()
    teams_count = Team.objects.count()
    workers_count = Worker.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    latest_tasks = Task.objects.filter(
        assignees=request.user,
        status__in=("TODO", "IN_PROGRESS")
    ).select_related(
        "project",
        "task_type"
    ).prefetch_related("assignees", "tags")[:6]
    completed_tasks = Task.objects.filter(
        assignees=request.user,
        status="DONE"
    ).select_related(
        "project",
        "task_type"
    ).prefetch_related("assignees", "tags")[:6]

    context = {
        "tasks_count": tasks_count,
        "projects_count": projects_count,
        "teams_count": teams_count,
        "workers_count": workers_count,
        "num_visits": num_visits + 1,
        "latest_tasks": latest_tasks,
        "completed_tasks": completed_tasks
    }

    return render(request, "tasks/index.html", context=context)


class BaseSearchListView(LoginRequiredMixin, generic.ListView):
    search_form_class = BaseNameSearchForm
    search_param = "query"
    search_fields = []

    def get_search_form(self):
        return self.search_form_class(self.request.GET)

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_search_form()

        if form.is_valid() and form.cleaned_data.get(self.search_param):
            value = form.cleaned_data[self.search_param]

            q_objects = None
            for field in self.search_fields:
                q = Q(**{f"{field}__icontains": value})
                q_objects = q if q_objects is None else q_objects | q

            return queryset.filter(q_objects)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.get_search_form()
        return context


class TagListView(BaseSearchListView):
    model = Tag
    context_object_name = "tag_list"
    paginate_by = 30
    search_fields = ["name"]


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag-list")


class TaskTypeListView(BaseSearchListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "tasks/task_type_list.html"
    paginate_by = 30
    search_fields = ["name"]


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task_type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task_type-list")


class TaskListView(BaseSearchListView):
    model = Task
    context_object_name = "task_list"
    paginate_by = 6
    search_form_class = TaskSearchForm
    search_fields = ["name", "description", "tags__name"]


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["available_workers"] = Worker.objects.exclude(
            tasks=self.object
        )

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class ProjectListView(BaseSearchListView):
    model = Project
    context_object_name = "project_list"
    paginate_by = 9
    search_form_class = ProjectSearchForm
    search_fields = ["name", "description", "tasks__name"]


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["available_tasks"] = Task.objects.exclude(
            project=self.object
        )

        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("tasks:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy(
            "tasks:project-detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:project-list")


class PositionListView(BaseSearchListView):
    model = Position
    context_object_name = "position_list"
    paginate_by = 30
    search_fields = ["name"]


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


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
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "tasks:worker-detail",
            kwargs={"pk": self.object.pk}
        )


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


class TeamListView(BaseSearchListView):
    model = Team
    context_object_name = "team_list"
    paginate_by = 9
    search_form_class = TeamSearchForm
    search_fields = ["name", "description", "workers__name"]


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blank_team = Team.objects.get(name="Blank")
        context["available_projects"] = Project.objects.filter(
            team=blank_team
        )

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("tasks:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("tasks:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:team-list")


class SendTaskToReview(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        task = get_object_or_404(Task, id=pk)
        if (
                request.user in task.assignees.all()
                and task.status not in ("DONE", "IN_REVIEW")
        ):
            task.status = "IN_REVIEW"
            task.save()
        return redirect("tasks:task-detail", pk=pk)


class ApproveTask(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        task = get_object_or_404(Task, id=pk)
        if (
            request.user.is_staff
            and task.status == "IN_REVIEW"
        ):
            task.status = "DONE"
            task.save()
        return redirect("tasks:task-detail", pk=pk)


class AddTaskToProject(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        project = get_object_or_404(Project, pk=pk)
        task_id = request.POST.get("task_id")

        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            task.project = project
            task.save()

        return redirect("tasks:project-detail", pk=pk)


class RemoveTaskFromProject(LoginRequiredMixin, generic.View):
    def post(self, request, pk: int, task_id: int):
        task = get_object_or_404(Task, pk=task_id)
        unassigned_project = get_object_or_404(Project, name="Unassigned")

        task.project = unassigned_project
        task.save()

        return redirect("tasks:project-detail", pk=pk)


class AddAssignee(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        task = get_object_or_404(Task, pk=pk)
        user_id = request.POST.get("worker_id")

        if user_id:
            worker = get_object_or_404(Worker, pk=user_id)
            task.assignees.add(worker)

        return redirect("tasks:task-detail", pk=pk)


class RemoveAssignee(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int, user_id: int):
        task = get_object_or_404(Task, pk=pk)
        worker = get_object_or_404(Worker, pk=user_id)

        if request.user.is_staff:
            task.assignees.remove(worker)

        return redirect("tasks:task-detail", pk=pk)


class TeamRemoveProject(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int, project_id: int):
        project = get_object_or_404(Project, pk=project_id)

        blank_team = get_object_or_404(Team, name="Blank")
        project.team = blank_team
        project.save()

        return redirect("tasks:team-detail", pk=pk)


class ToggleAssignToTeam(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        worker = request.user
        if worker.teams.filter(pk=pk).exists():
            worker.teams.remove(pk)
        else:
            worker.teams.add(pk)
        return redirect("tasks:team-detail", pk=pk)


class AddProjectToTeam(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        team = get_object_or_404(Team, pk=pk)
        project_id = request.POST.get("project_id")

        if project_id:
                project = get_object_or_404(Project, pk=project_id)
                project.team = team
                project.save()

        return redirect("tasks:team-detail", pk=pk)
