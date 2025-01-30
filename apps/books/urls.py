from django.urls import path
from apps.books import views

# Book URLs
urlpatterns = [
    path("genre", views.ListCreateGenreView.as_view()),
    path("author", views.ListCreateAuthorView.as_view()),

    path("book", views.ListCreateBookView.as_view()),
    path("book/<str:book_id>", views.RetrieveUpdateDestroyBookView.as_view()),
]