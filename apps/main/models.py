from django.db import models

from apps.ausers.models import User
from apps.books.models import Book
from core.base.models import BaseModel


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[
        (i, str(i)) for i in range(6)  # 0-5
    ])
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'book')  # Foydalanuvchi bitta kitobni faqat bir marta baholay oladi

    def __str__(self):
        return f"{self.user.full_name} → {self.book.title} ({self.rating})"
