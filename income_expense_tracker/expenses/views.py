from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'expenses/index.html')

def add_expense(request):
    return render(request, 'expenses/add_expense.html')
