from django.urls import path
from apps.orders import views


# Order URLs
urlpatterns = [
    path("order", views.ListCreateOrderView.as_view()),
    path("order/<str:order_id>", views.RetrieveUpdateOrderView.as_view()),
]
