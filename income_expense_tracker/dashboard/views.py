from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from expenses.models import Expense


# This function can only be accessed after logging in.
@login_required(login_url="/authentication/login")
def index(request):
    """This function renders the home page with context data."""

    # Gets every expenses of current user.
    expenses = Expense.objects.filter(owner=request.user)
    # Returns a QuerySet that contains dictionary.
    data = expenses.values()
    totalAmount = 0  # amount variable.

    # For loop that iterates over data list and adds amount to totalAmount.
    for value in data:
        totalAmount += value['amount']

    # variable value mapping that is passed to the home template.
    context = {
        "amount": totalAmount,
        "expenses": data[::-1][0:5]
    }
    # Returns the home page.
    return render(request, "dashboard/index.html", context)
