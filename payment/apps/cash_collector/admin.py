from django.contrib import admin
from .models import CashCollector, Task, CollectionRecord


@admin.register(CashCollector)
class CashCollectorAdmin(admin.ModelAdmin):
    list_display = ("user", "is_frozen")
    list_filter = ("is_frozen",)
    search_fields = ("user__username", "user__email")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "amount_due", "amount_due_at")
    list_filter = ("amount_due_at",)
    search_fields = ("customer_name",)

    date_hierarchy = 'amount_due_at'


@admin.register(CollectionRecord)
class CollectionRecordAdmin(admin.ModelAdmin):
    list_display = ("collector", "amount_collected", "collected_at")
    list_filter = ("collected_at",)
    search_fields = ("collector__user__username", "amount_collected")
    date_hierarchy = 'collected_at'
