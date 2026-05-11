from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tasks.models import Task, Project, Team, Worker


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
        assignee=request.user,
        status__in=("TODO", "IN_PROGRESS")
    )[:6]

    context = {
        "tasks_count": tasks_count,
        "projects_count": projects_count,
        "teams_count": teams_count,
        "workers_count": workers_count,
        "num_visits": num_visits + 1,
        "latest_tasks": latest_tasks
    }

    return render(request, "tasks/index.html", context=context)
