from django.contrib import admin

from apps.orders.models import Order, Booked


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "order_date", "due_date", "return_date", "fine"]
    readonly_fields = ["calculate_fine"]


@admin.register(Booked)
class BookedAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "reserved_at"]
    readonly_fields = ["reserved_at"]
