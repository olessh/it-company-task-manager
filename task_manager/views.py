from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import Position, TaskType, Task, Worker
from task_manager.forms import TaskForm, WorkerCreationForm, WorkerPositionUpdateForm


@login_required
def index(request):
    num_positions = Position.objects.count()
    num_task_types = TaskType.objects.count()
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_positions": num_positions,
        "num_task_types": num_task_types,
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_visits": num_visits + 1
    }

    return render(request, "task_manager/index.html", context=context)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
    template_name = "task_manager/position_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
    template_name = "task_manager/position_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")
    template_name = "task_manager/position_confirm_delete.html"


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type")
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_confirm_delete.html"


@login_required()
def update_task_assignee(request, pk):
    task = Task.objects.get(id=pk)
    assignee = request.user
    if assignee in task.assignees.all():
        task.assignees.remove(assignee)
    else:
        task.assignees.add(assignee)
    return redirect(task)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position").prefetch_related("tasks", "tasks__task_type")
    template_name = "task_manager/worker_detail.html"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdatePositionView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm
