from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        "categories": categories,
        "expenses": expenses,
        "page_obj": page_obj
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url="/authentication/login")
def add_expense(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        'values': request.POST
    }
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            print("TIMEEEEEEEEEE", datetime.utcnow())
            messages.error(request, "Please add an amount.")
            return render(request, 'expenses/add_expense.html', context)

        description = request.POST['description']
        category = request.POST['category']

        date = request.POST['expense_date']
        if not date:
            date = now().date()

        Expense.objects.create(
            amount=amount,
            date=date,
            category=category,
            description=description,
            owner=request.user
        )

        messages.success(request, "Expense saved successfully.")
        return redirect('expenses')
    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url="/authentication/login")
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
    }

    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Please add an amount.")
            return render(request, 'expenses/edit_expense.html', context)

        description = request.POST['description']
        category = request.POST['category']

        date = request.POST['expense_date']
        if not date:
            date = now().date()

        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=description
        expense.owner=request.user
        expense.save()

        messages.success(request, "Expense updated successfully.")
        return redirect('expenses')

    return render(request, 'expenses/edit_expense.html', context)


@login_required(login_url="/authentication/login")
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted.")
    return redirect('expenses')

def filter_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('filter_by')
        expenses = Expense.objects.filter(category=search_str, owner=request.user).order_by('-date')
        data = expenses.values()
        # return the list of values. Since JsonResponse usually sends dict type,
        # we set safe=False which allows list to be send
        return JsonResponse(list(data), safe=False)
