from django.test import TestCase

from task_manager.forms import WorkerCreationForm
from task_manager.models import Position


class FormsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_creation_form_with_position_first_last_name_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "position": self.position,
            "first_name": "Test First",
            "last_name": "Test Last"
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
