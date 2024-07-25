from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from task_manager.models import Position, TaskType, Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()

    context = {
        "num_positions": num_positions,
        "num_task_types": num_task_types,
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }

    return render(request, "task_manager/index.html", context=context)


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 5


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type")
    paginate_by = 5


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position").prefetch_related("tasks", "tasks__task_type")
    template_name = "task_manager/worker_detail.html"
