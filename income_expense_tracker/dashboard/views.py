from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from expenses.models import Expense


@login_required(login_url="/authentication/login")
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    data = expenses.values()
    amount = 0
    for value in data:
        amount += value['amount']
    context = {
        "amount": amount,
        "expenses": data[::-1][0:5]
    }
    return render(request, "dashboard/index.html", context)
