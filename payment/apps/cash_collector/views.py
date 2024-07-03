from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .serializers import (
    CashCollectorStatusSerializer,
    CollectAmountSerializer,
    TaskSerializer,
    PayAmountSerializer,
)
from .models import Task, CollectionRecord, CashCollector
from .validations import CashCollectorFrozenError


class CashCollectorStatusView(generics.RetrieveAPIView):
    queryset = CashCollector.objects.all()
    serializer_class = CashCollectorStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cash_collector = CashCollector.objects.get(user=user)
        total_collected = sum(
            record.amount_collected
            for record in cash_collector.collection_records.all()
        )
        two_days_ago = timezone.now() - timedelta(days=settings.CASH_THRESHOLD_DAYS)
        if total_collected > settings.CASH_THRESHOLD_AMOUNT:
            first_exceeding_record = (
                cash_collector.collection_records.filter(collected_at__lte=two_days_ago)
                .order_by("collected_at")
                .first()
            )
            if first_exceeding_record:
                cash_collector.is_frozen = True
                cash_collector.frozen_since = first_exceeding_record.collected_at
            else:
                cash_collector.is_frozen = False
                cash_collector.frozen_since = None
        else:
            cash_collector.is_frozen = False
            cash_collector.frozen_since = None
        cash_collector.save()
        return cash_collector


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(collector__user=user)


class NextTaskAPIView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        collector = user.cash_collector
        now = timezone.now()
        next_task = (
            Task.objects.filter(
                collector=collector, is_completed=False, amount_due_at__lte=now
            )
            .order_by("amount_due_at")
            .first()
        )
        return next_task


class CashCollectorStatusAPIView(generics.RetrieveAPIView):
    serializer_class = CashCollectorStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cash_collector = CashCollector.objects.get(user=user)
        return cash_collector


class CollectAmountAPIView(generics.CreateAPIView):
    serializer_class = CollectAmountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        task_id = serializer.validated_data["task_id"]
        amount_collected = serializer.validated_data["amount_collected"]

        task = get_object_or_404(Task, id=task_id)
        collector = get_object_or_404(CashCollector, user=user)

        if not collector.is_frozen:
            CollectionRecord.objects.create(
                collector=collector,
                amount_collected=amount_collected,
                collected_at=task.amount_due_at,
            )
        else:
            raise CashCollectorFrozenError

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except CashCollectorFrozenError:
            return Response(
                CashCollectorFrozenError.to_json(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
