from django.contrib import admin

from apps.orders.models import Order, Reservation


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "order_date", "due_date", "return_date", "fine"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "reserved_at"]
    readonly_fields = ["reserved_at"]
