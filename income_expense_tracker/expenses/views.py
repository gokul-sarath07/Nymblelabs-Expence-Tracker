from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from .models import Expense, Category


# This function can only be accessed after logging in.
@login_required
def index(request):
    """This function deals with expenses template functionality."""

    # Gets all category from the category database.
    categories = Category.objects.all()

    # Gets all expenses of current user in from database
    # ordered in reverse by date.
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    number_of_records_per_page = 5
    # Creates a paginator object with expenses data
    paginator = Paginator(expenses, number_of_records_per_page)
    page_number = request.GET.get('page')  # gets page number from request.
    # Creates a page number object for paginator.
    page_obj = Paginator.get_page(paginator, page_number)
    # variable value mapping that is passed to the expenses template.
    context = {
        "categories": categories,
        "expenses": expenses,
        "page_obj": page_obj
    }
    return render(request, 'expenses/index.html', context)


# This function can only be accessed after logging in.
@login_required
def add_expense(request):
    """This function deals with add expenses template functionality."""

    # Gets all category from database.
    categories = Category.objects.all()
    # variable value mapping that is passed to the add expenses template.
    context = {
        "categories": categories,
        'values': request.POST
    }
    # Checks if request method is POST.
    if request.method == "POST":
        amount = request.POST['amount']  # Gets amount from request.
        # Checks if amount is empty.
        if not amount:
            # Sends error message to user for empty field.
            messages.error(request, "Please add an amount.")
            return render(request, 'expenses/add_expense.html', context)

        # Checks if amount is less than 0.
        if int(amount) < 0:
            # Sends error message to user for invalid value.
            messages.error(request, "Please add a positive number.")
            return render(request, 'expenses/add_expense.html', context)

        # Gets description from request.
        description = request.POST['description']
        category = request.POST['category']  # Gets category from request.

        date = request.POST['expense_date']  # Gets date from request.
        # Checks if date is empty.
        if not date:
            # if it is, then assign todays date.
            date = now().date()

        # Creats a new expense record.
        Expense.objects.create(
            amount=amount,
            date=date,
            category=category,
            description=description,
            owner=request.user
        )

        # Sends success message to user for successfully creation.
        messages.success(request, "Expense saved successfully.")
        return redirect('expenses')
    # Returns add expenses template for GET request.
    return render(request, 'expenses/add_expense.html', context)


# This function can only be accessed after logging in.
@login_required
def edit_expense(request, id):
    """This function deals with edit expenses template functionality."""

    # Gets expense with ID from expenses database.
    expense = Expense.objects.get(pk=id)
    # Gets all category from the category database.
    categories = Category.objects.all()
    # variable value mapping that is passed to the edit expenses template.
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
    }

    # Checks if request method is POST.
    if request.method == "POST":
        amount = request.POST['amount']  # Gets amount from request.
        # Checks if amount is empty.
        if not amount:
            # Sends error message to user for empty field.
            messages.error(request, "Please add an amount.")
            return render(request, 'expenses/edit_expense.html', context)

        # Checks if amount is less than 0.
        if int(amount) < 0:
            # Sends error message to user for invalid value.
            messages.error(request, "Please add a positive number.")
            return render(request, 'expenses/edit_expense.html', context)

        # Gets description from request.
        description = request.POST['description']
        category = request.POST['category']  # Gets category from request.

        date = request.POST['expense_date']  # Gets date from request.
        # Checks if date is empty.
        if not date:
            # if it is, then assign todays date.
            date = now().date()

        # Updates the current record with new data.
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.owner = request.user
        expense.save()  # Saves the record.

        # Sends success message to user for successfully updation.
        messages.success(request, "Expense updated successfully.")
        return redirect('expenses')
    # Returns edit expenses template for GET request.
    return render(request, 'expenses/edit_expense.html', context)


# This function can only be accessed after logging in.
@login_required
def delete_expense(request, id):
    """This function deals with delete expenses template functionality."""

    # Gets expense with ID from expenses database.
    expense = Expense.objects.get(pk=id)
    expense.delete()  # Deletes the selected expense.
    # Sends success message to user for successfully delection.
    messages.success(request, "Expense deleted.")
    return redirect('expenses')


def filter_expenses(request):
    """This function is an API View for filtering data."""

    # Checks if request method is POST.
    if request.method == "POST":
        # Gets the search_str form request body with key as 'filter_by'.
        search_str = json.loads(request.body).get('filter_by')
        # Gets all expenses from database for which the
        # category matches the search_str and the owner is the current user,
        # ordered by date in reverse.
        expenses = Expense.objects.filter(category=search_str,
                                          owner=request.user).order_by('-date')
        # Returns a QuerySet that contains dictionary.
        data = expenses.values()

        # return the list of values. Since JsonResponse usually
        # sends dict type, we set safe=False which allows list to be send.
        return JsonResponse(list(data), safe=False)
