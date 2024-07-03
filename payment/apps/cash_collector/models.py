from django.db import models
from django.contrib.auth.models import User


class CashCollector(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cash_collector"
    )
    is_frozen = models.BooleanField(default=False)
    frozen_since = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.pk}, user={self.user.username}, is_frozen={self.is_frozen})"


class Task(models.Model):
    collector = models.ForeignKey(
        CashCollector,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    customer_name = models.CharField(max_length=255)
    address = models.TextField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.pk}, customer_name={self.customer_name}, is_completed={self.is_completed})"


class CollectionRecord(models.Model):
    collector = models.ForeignKey(
        CashCollector, on_delete=models.CASCADE, related_name="collection_records"
    )
    amount_collected = models.DecimalField(max_digits=10, decimal_places=2)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.pk}, amount_collected={self.amount_collected}) "
            f"by {self.collector} at [{self.collected_at}]"
        )
