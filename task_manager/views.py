from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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
