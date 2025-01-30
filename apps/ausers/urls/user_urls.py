from django.urls import path

from apps.ausers import views


urlpatterns = [
    path("detail", views.GetUserDetailView.as_view()),
    path("update", views.UpdateUserDetailView.as_view()),
]
