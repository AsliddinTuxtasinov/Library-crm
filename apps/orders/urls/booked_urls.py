from django.urls import path
from apps.orders import views


# Booked (Reservation) URLs
urlpatterns = [
    path("create-booked", views.CreateBookedView.as_view()),
    path("list-booked", views.ListBookedView.as_view()),
]
