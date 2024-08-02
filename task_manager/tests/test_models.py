from datetime import datetime
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType, Task, Position, Worker


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.task_type = TaskType.objects.create(name="Bug")
        cls.worker = Worker.objects.create_user(
            username="olesshulzh",
            password="2405",
            first_name="Oles",
            last_name="Shulzhenko",
            position=cls.position
        )

        cls.task = Task.objects.create(
            name="Test Task",
            description="This is a test task description.",
            deadline=datetime(2024, 8, 8, 12, 0, 0),
            is_completed=False,
            priority=Task.Priority.MEDIUM,
            task_type=cls.task_type
        )
        cls.task.assignees.add(cls.worker)

    def test_position_str(self):
        position = self.position
        self.assertEqual(str(position), position.name)

    def test_task_type_str(self):
        task_type = self.task_type
        self.assertEqual(str(task_type), task_type.name)

    def test_task_str(self):
        task = self.task
        self.assertEqual(str(task), f"{task.name} ({task.get_priority_display()}) - "
                                    f"{'Completed' if task.is_completed else 'Incomplete'} - "
                                    f"Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M:%S')}")

    def test_task_get_absolute_url(self):
        self.assertEqual(
            self.task.get_absolute_url(),
            reverse("task_manager:task-detail", kwargs={"pk": self.task.pk}))

    def test_worker_str(self):
        worker = self.worker
        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.position})"
        )

    def test_create_worker_width_position(self):
        worker = self.worker
        self.assertEqual(str(worker.username), "olesshulzh")
        self.assertEqual(str(worker.position.name), "Developer")
        self.assertTrue(worker.check_password("2405"))

    def test_worker_get_absolute_url(self):
        self.assertEqual(
            self.worker.get_absolute_url(),
            reverse("task_manager:worker-detail", args=[self.worker.id]))
