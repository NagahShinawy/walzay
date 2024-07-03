from rest_framework import serializers
from .models import CashCollector, Task
from .validations import ValidateTaskId, ValidateAmountCollected
from ..accounts.serializers import UserSerializer


class CashCollectorStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CashCollector
        fields = ["user", "is_frozen", "frozen_since"]
        depth = 1


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "customer_name", "address", "amount_due", "amount_due_at"]


class CollectAmountSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    amount_collected = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_task_id(self, value):
        try:
            _ = Task.objects.get(id=value)
        except Task.DoesNotExist:
            ValidateTaskId.raise_error()
        return value

    def validate(self, data):
        task_id = data.get("task_id")
        amount_collected = data.get("amount_collected")
        task = Task.objects.get(id=task_id)

        if amount_collected > task.amount_due:
            ValidateAmountCollected.raise_error()

        return data


class PayAmountSerializer(serializers.Serializer):
    amount_delivered = serializers.DecimalField(max_digits=10, decimal_places=2)
