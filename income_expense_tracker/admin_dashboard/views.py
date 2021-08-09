from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from expenses.models import Expense

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    # Gets all users from the users database.
    users = User.objects.all()
    # Gets all expenses of all user from the database
    # ordered in reverse by date.
    expenses = Expense.objects.all().order_by('-date')
    number_of_records_per_page = 5
    # Creates a paginator object with expenses data
    paginator = Paginator(expenses, number_of_records_per_page)
    page_number = request.GET.get('page')  # gets page number from request.
    # Creates a page number object for paginator.
    page_obj = Paginator.get_page(paginator, page_number)
    # variable value mapping that is passed to the expenses template.
    context = {
        "users": users,
        "expenses": expenses,
        "page_obj": page_obj
    }
    return render(request, 'admin_dashboard/index.html', context)

@user_passes_test(lambda u: u.is_superuser)
def filter_users(request):
    """This function is an API View for filtering data."""

    # Checks if request method is POST.
    if request.method == "POST":
        # Gets the search_str form request body with key as 'filter_by'.
        search_str = json.loads(request.body).get('filter_by')
        # Get the user id  of the user for which the search_str matches.
        user_id = User.objects.filter(username=search_str)[0].id
        # Gets all expenses from database for which the
        # owner matches the user id, ordered by date in reverse.
        expenses = Expense.objects.filter(owner=user_id).order_by('-date')
        # Returns a QuerySet that contains dictionary.
        data = expenses.values()

        # return the list of values. Since JsonResponse usually
        # sends dict type, we set safe=False which allows list to be send.
        return JsonResponse(list(data), safe=False)
