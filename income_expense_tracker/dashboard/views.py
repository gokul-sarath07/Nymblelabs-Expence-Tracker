from django.shortcuts import render
from expenses.models import Expense
from django.http import JsonResponse


# Create your views here.
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
