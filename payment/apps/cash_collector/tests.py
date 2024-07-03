from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.cash_collector.models import CashCollector, Task, CollectionRecord


class CashCollectorStatusAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cash_collector = CashCollector.objects.create(
            user=self.user, is_frozen=False
        )

    def test_get_cash_collector_status(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("cashcollector-status")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], self.user.username)
        self.assertEqual(response.data["is_frozen"], self.cash_collector.is_frozen)

    def test_get_cash_collector_status_unauthenticated(self):
        url = reverse("cashcollector-status")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskListAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cash_collector = CashCollector.objects.create(user=self.user)
        self.task1 = Task.objects.create(
            customer_name="Customer 1",
            address="Address 1",
            amount_due=100.0,
            amount_due_at="2024-07-05T10:00:00Z",
            collector=self.cash_collector,
        )
        self.task2 = Task.objects.create(
            customer_name="Customer 2",
            address="Address 2",
            amount_due=200.0,
            amount_due_at="2024-07-06T10:00:00Z",
            collector=self.cash_collector,
        )

    def test_get_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 2
        )  # Assuming two tasks are returned
        self.assertEqual(
            response.data["results"][0]["customer_name"], self.task1.customer_name
        )
        self.assertEqual(
            response.data["results"][1]["customer_name"], self.task2.customer_name
        )

    def test_get_tasks_unauthenticated(self):
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NextTaskAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cash_collector = CashCollector.objects.create(user=self.user)

    def test_get_next_task_authenticated_no_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("next-task")
        response = self.client.get(url)
        self.assertEqual(
            response.data,
            {
                "customer_name": "",
                "address": "",
                "amount_due": None,
                "amount_due_at": None,
            },
        )

    def test_get_next_task_authenticated_with_task(self):
        now = timezone.now()
        task1 = Task.objects.create(
            customer_name="Customer 1",
            address="Address 1",
            amount_due=100.0,
            amount_due_at=now,
            collector=self.cash_collector,
        )

        self.client.force_authenticate(user=self.user)
        url = reverse("next-task")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], task1.id)
        self.assertEqual(response.data["customer_name"], task1.customer_name)


class CollectAmountAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cash_collector = CashCollector.objects.create(user=self.user)

        self.task1 = Task.objects.create(
            customer_name="Customer 1",
            address="Address 1",
            amount_due=100.0,
            amount_due_at="2024-07-05T10:00:00Z",
            collector=self.cash_collector,
        )

    def test_collect_amount_valid(self):
        url = reverse("collect-amount")
        data = {
            "task_id": self.task1.id,
            "amount_collected": 80.0,  # Collecting less than the amount due
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CollectionRecord.objects.count(), 1)
        self.assertEqual(CollectionRecord.objects.first().amount_collected, 80.0)

    def test_collect_amount_invalid_task_id(self):
        url = reverse("collect-amount")
        data = {
            "task_id": 999,  # Invalid task ID
            "amount_collected": 50.0,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Task with this ID does not exist.", response.data["task_id"])

    def test_collect_amount_exceeds_due_amount(self):
        url = reverse("collect-amount")
        data = {
            "task_id": self.task1.id,
            "amount_collected": 150.0,  # Collecting more than the amount due
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Amount collected cannot be greater than amount due.",
            response.data["non_field_errors"],
        )

    def test_collect_amount_collector_frozen(self):
        self.cash_collector.is_frozen = True
        self.cash_collector.save()

        url = reverse("collect-amount")
        data = {
            "task_id": self.task1.id,
            "amount_collected": 50.0,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "CashCollector is frozen and cannot collect more cash.",
            response.data["error"],
        )
