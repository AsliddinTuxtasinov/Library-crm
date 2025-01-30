from django.urls import path
from apps.main import views


urlpatterns = [
    path("create-review", views.CreateReviewView.as_view()),
    path("get-review/<str:book_id>", views.ListReviewsByBookIdView.as_view()),
]
