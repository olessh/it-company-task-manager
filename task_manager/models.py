from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "L", "Low"
        MEDIUM = "M", "Medium"
        HIGH = "H", "High"
        URGENT = "U", "Urgent"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ("deadline", )

    def get_absolute_url(self):
        return reverse("task_manager:task-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return (f"{self.name} ({self.get_priority_display()}) - "
                f"{'Completed' if self.is_completed else 'Incomplete'} - "
                f"Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}")


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ("username", )
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def get_absolute_url(self) -> str:
        return reverse("task_manager:worker-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.username} ({self.position})"
