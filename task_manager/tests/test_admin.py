from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position, Task, TaskType


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin",
            position=self.position
        )
        self.client.force_login(self.admin_user)

        self.worker = get_user_model().objects.create_user(
            username="olesshulzh",
            password="2405",
            first_name="Oles",
            last_name="Shulzhenko",
            position=self.position
        )

        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test task description.",
            deadline=datetime(2024, 8, 8, 12, 0, 0),
            is_completed=False,
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type
        )

    def test_worker_position_listed(self):
        """
        Test that worker's position is in list_display
        on worker admin page
        :return:
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position.name)

    def test_worker_detail_position_listed(self):
        """
        Test that worker's position is in list_display
        on worker detail admin page
        :return:
        """
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position.name)

    def test_worker_add_fieldsets(self):
        """
        Test that worker's first_name, last_name, position
        is in add_fieldsets on worker add admin page
        :return:
        """
        url = reverse("admin:task_manager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, 'name="first_name"')
        self.assertContains(res, 'name="last_name"')
        self.assertContains(res, 'name="position"')

    def assert_task_fields(self, response, task):
        self.assertContains(response, task.name)
        self.assertContains(response, task.task_type.name)
        self.assertContains(response, task.get_priority_display())
        self.assertContains(response, task.deadline.strftime("%Y-%m-%d %H:%M:%S"))

    def test_task_list_display(self):
        """
        Test that task's fields are in list_display
        on task admin page
        :return:
        """
        url = reverse("admin:task_manager_task_changelist")
        res = self.client.get(url)
        self.assert_task_fields(res, self.task)
        self.assertContains(res, self.task.is_completed)

    def test_task_detail_display(self):
        """
        Test that task's fields are displayed on task detail admin page
        :return:
        """
        url = reverse("admin:task_manager_task_change", args=[self.task.id])
        res = self.client.get(url)
        self.assert_task_fields(res, self.task)
        if self.task.is_completed:
            self.assertContains(res, "checked", html=True)
        else:
            self.assertNotContains(res, "checked", html=True)
