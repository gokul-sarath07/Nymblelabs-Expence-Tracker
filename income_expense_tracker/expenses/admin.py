from django.contrib import admin

from .models import Expense, Category


class ExpenseAdmin(admin.ModelAdmin):
    """
    - Changes the display fields of the Expense model
      in the django admin.
    - Adds a search field and defines the search category
      of the Expense Model.
    """
    list_display = ('owner', 'category', 'amount', 'description', 'date')
    search_fields = ('category', 'date', 'description')


# Registering both models to the django admin.
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
