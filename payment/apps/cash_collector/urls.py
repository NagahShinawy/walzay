from django.urls import path
from .views import (
    CashCollectorStatusAPIView,
    TaskListAPIView,
    NextTaskAPIView,
    CollectAmountAPIView,
)

urlpatterns = [
    path("status/", CashCollectorStatusAPIView.as_view(), name="cashcollector-status"),
    path("tasks/", TaskListAPIView.as_view(), name="task-list"),
    path("next_task/", NextTaskAPIView.as_view(), name="next-task"),
    path("collect/", CollectAmountAPIView.as_view(), name="collect-amount"),
]
