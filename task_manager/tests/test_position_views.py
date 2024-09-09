from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import PositionSearchForm
from task_manager.models import Position

POSITION_URL = reverse("task_manager:position-list")


class PublicPositionTest(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_position(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_search_functionality(self):
        response = self.client.get(POSITION_URL, {"name": "Developer"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("position_list" in response.context)
        self.assertEqual(len(response.context["position_list"]), 1)
        self.assertEqual(
            response.context["position_list"][0].name,
            "Developer"
        )

    def test_search_form_in_context(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(
            response.context["search_form"],
            PositionSearchForm
        )
