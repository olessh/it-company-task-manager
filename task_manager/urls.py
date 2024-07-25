from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from task_manager.views import (
    index,
    PositionListView,
    TaskTypeListView,
    TaskListView,
    TaskDetailView,
    WorkerListView,
    WorkerDetailView
)

app_name = "task_manager"

urlpatterns = [
    path("", index, name="index"),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
