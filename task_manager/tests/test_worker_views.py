from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse
from task_manager.models import Worker, Position
from task_manager.forms import WorkerSearchForm


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_create_worker(self):
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "position": self.position.id,
            "first_name": "Test First",
            "last_name": "Test Last"
        }
        self.client.post(reverse("task_manager:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position, self.position)


WORKER_URL = reverse("task_manager:worker-list")


class WorkerListViewTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_worker(self):
        Worker.objects.create(
            username="olesshulzh",
            password="2405",
            first_name="Oles",
            last_name="Shulzhenko",
            position=self.position
        )
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        workers = Worker.objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_search_functionality(self):
        number_of_workers = 5
        for worker_id in range(number_of_workers):
            Worker.objects.create(
                username=f"testuser{worker_id}",
                position=self.position,
                first_name=f"First{worker_id}",
                last_name=f"Last{worker_id}"
            )
        response = self.client.get(WORKER_URL, {"username": "testuser1"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("worker_list" in response.context)
        self.assertEqual(len(response.context["worker_list"]), 1)
        self.assertEqual(
            response.context["worker_list"][0].username,
            "testuser1"
        )

    def test_search_form_in_context(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            WorkerSearchForm
        )
