from django.contrib import admin

from apps.main.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "rating"]
