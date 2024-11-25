from django.contrib import admin
from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'owner', 'amount', 'category', 'description')
    search_fields = ('date', 'owner__username', 'amount', 'description')  # Adjusted category field
    list_per_page=10
# Register your models here.
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
