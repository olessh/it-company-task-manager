from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import TaskTypeSearchForm
from task_manager.models import TaskType, Position

TASK_TYPE_URL = reverse("task_manager:task-type-list")


class PublicTaskTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_task_type(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(response.context["object_list"]),
            list(task_types)
        )
        self.assertTemplateUsed(response, "task_manager/task_type_list.html")

    def test_search_functionality(self):
        response = self.client.get(TASK_TYPE_URL, {"name": "Bug"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("object_list" in response.context)
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(
            response.context["object_list"][0].name,
            "Bug"
        )

    def test_search_form_in_context(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            TaskTypeSearchForm
        )
