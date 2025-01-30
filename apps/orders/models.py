from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.ausers.models import User
from apps.books.models import Book
from core.base.models import BaseModel


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()  # Kitobni topshirish sanasi
    return_date = models.DateTimeField(null=True, blank=True)  # Haqiqiy qaytarilgan sana
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        """ Kitob bron qilingan bo‘lsa, avtomatik mavjudlikni o‘zgartirish """
        if not self.pk:
            self.book.available = False
            self.book.save()
        super().save(*args, **kwargs)

    def calculate_fine(self,):
        """ Agar muddati o‘tgan bo‘lsa, jarima hisoblash """
        if self.return_date and self.return_date > self.due_date:
            overdue_days = (self.return_date - self.due_date).days
            return round(self.book.daily_price * 0.01 * overdue_days, 2)
        return 0

    def mark_as_returned(self):
        """ Kitob qaytarilganda jarima hisoblab, mavjudlikni yangilash """
        self.return_date = timezone.now()
        self.fine = self.calculate_fine()

        self.book.available = True
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.user.full_name} - {self.book.title} ({self.order_date.date()})"

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Reservation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """ Agar 24 soatdan oshib ketgan bo‘lsa, bron bekor qilinadi """
        return timezone.now() > self.reserved_at + timedelta(days=1)

    def save(self, *args, **kwargs):
        """ Yangi obyekt yaratishda kitobni mavjud emas deb belgilash """
        if self._state.adding:  # Yangi obyekt yaratilyaptimi?
            self.book.available = False
            self.book.save()

        super().save(*args, **kwargs)

    def cancel_reservation(self):
        """ Agar foydalanuvchi kitobni olib ketmasa, bronni bekor qilish """
        if self.is_expired():
            self.book.available = True
            self.book.save()
            self.delete()

    def __str__(self):
        return f"{self.user.full_name} → {self.book.title} (Reserved on {self.reserved_at.date()})"

    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
