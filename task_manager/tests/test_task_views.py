from datetime import datetime
from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse
from task_manager.models import Position, TaskType, Task
from task_manager.forms import TaskSearchForm

TASK_URL = reverse("task_manager:task-list")


class PublicTaskTest(TestCase):
    def test_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

        number_of_tasks = 5
        for task_id in range(number_of_tasks):
            Task.objects.create(
                name=f"Test Task{task_id}",
                description=f"This is the test task {task_id} description.",
                deadline=datetime(2024, 8, 8, 12, 0, 0),
                is_completed=False,
                priority=Task.Priority.MEDIUM,
                task_type=self.task_type
            )

    def test_retrieve_tasks(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_search_functionality(self):
        response = self.client.get(TASK_URL, {"name": "Test Task3"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("task_list" in response.context)
        self.assertEqual(len(response.context["task_list"]), 1)
        self.assertEqual(
            response.context["task_list"][0].name,
            "Test Task3"
        )

    def test_search_form_in_context(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            TaskSearchForm
        )
