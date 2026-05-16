from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from core.forms import BaseNameSearchForm
from work.models import Task, Project
from users.models import Team, Worker


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

    return render(request, "core/index.html", context=context)


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

