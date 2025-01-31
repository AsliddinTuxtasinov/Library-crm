from datetime import timedelta

from celery import shared_task
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.utils import timezone

from apps.orders.models import Booked


@shared_task
def check_daily_bookings():

    expired_bookings = Booked.objects.annotate(
        expired=ExpressionWrapper(
            expression=F("reserved_at") + timedelta(days=1),
            output_field=DateTimeField()
        )
    ).filter(expired__lte=timezone.now())

    for booking in expired_bookings:
        booking.cancel_booked()

    return "checked all bookings !!!"


@shared_task
def add(a, b):
    return a + b
