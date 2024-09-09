from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Position, TaskType, Task, Worker

admin.site.register(Position)

admin.site.register(TaskType)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ["task_type", "priority",]
    search_fields = ["name",]
    list_display = [
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed"
    ]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_filter = ["position", ]
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": (
            "last_name",
            "first_name",
            "position",
        )}),
    )
