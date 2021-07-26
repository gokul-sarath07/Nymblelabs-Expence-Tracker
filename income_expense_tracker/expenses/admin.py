from django.contrib import admin

from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('owner', 'category', 'amount', 'description', 'date')
    search_fields = ('category', 'date', 'description')


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
