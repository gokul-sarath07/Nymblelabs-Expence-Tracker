from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import datetime
import calendar

from expenses.models import Expense


# This function can only be accessed after logging in.
@login_required
def stats_view(request):
    """This function renders the reports template."""

    return render(request, 'report/index.html')


def get_current_month_start_and_end_date():
    """
    This is a utility function which helps to get
    start date and end date of the current month.
    """
    todays_date = datetime.date.today()  # Gets todays date.
    # Seperates the year, month and day from todays_date.
    year, month, day = str(todays_date).split('-')
    # Gets number of days in the current month, which is also
    # the last day of the month.
    _, last_day_of_month = calendar.monthrange(int(year), int(month))
    # Returns DateTime value of start_date.
    start_date = datetime.date(int(year), int(month), 1)
    # Returns DateTime value of end_date.
    end_date = datetime.date(int(year), int(month), last_day_of_month)
    # Return both start_date and end_date.
    return start_date, end_date


def category_summery(request):
    """
    This function is an API View that returns a JsonResponse with
    a dictionary with key as category and value as total sum of amount
    of that category from Expense Model.
    """

    # Gets the start_date and end_date of current month.
    start_date, end_date = get_current_month_start_and_end_date()
    # Gets all expenses between these two dates and of the current user
    # ordered by date in reverse.
    expenses = Expense.objects.filter(date__gte=start_date,
                                      date__lte=end_date,
                                      owner=request.user).order_by('-date')
    final_form = {}  # final_form variable.

    def get_category(expense):
        """A utility function that returns the category of an expense"""

        return expense.category

    def get_category_amount(category):
        """
        A utility function that returns total sum of amount of a given category
        from filtered Expense Model.
        """
        totalAmount = 0  # amount variable.
        # Gets the required category datas from filtered expense queryset.
        filter_expenses_by_category = expenses.filter(category=category)
        # For loop that iterates over filter_expenses_by_category and
        # adds the amount of an item to the amount variable.
        for item in filter_expenses_by_category:
            totalAmount += item.amount
        # Returns the total amount
        return totalAmount

    # Gets all category in the filtered expenses queryset.
    category_list = list(set(map(get_category, expenses)))
    # For loop that iterates over category_list and adds total sum of amount
    # of that category from the filtered expenses queryset.
    for category in category_list:
        final_form[category] = get_category_amount(category)
    # Return JsonResponse with required data.
    return JsonResponse({'expense_category_data': final_form}, safe=False)


def weekly_summery(request):
    """
    This function is an API View that returns a JsonResponse with
    a dictionary with key as week number and value as total sum of amount of
    expenses per week from Expense Model.
    """

    # Gets the start_date and end_date of current month.
    start_date, end_date = get_current_month_start_and_end_date()
    # Gets all expenses between these two dates and of the current user
    # ordered by date in reverse.
    expenses = Expense.objects.filter(date__gte=start_date,
                                      date__lte=end_date,
                                      owner=request.user).order_by('-date')

    # Seperates the year, month and day from start_date.
    start_year, start_month, start_day = map(int, str(start_date).split('-'))
    # Seperates the year, month and day from end_date.
    end_year, end_month, end_day = map(int, str(end_date).split('-'))

    # Gets the week number of the start_date.
    start_week_number = datetime.date(start_year,
                                      start_month,
                                      start_day).isocalendar()[1]
    # Gets the week number of the end_date.
    end_week_number = datetime.date(end_year,
                                    end_month,
                                    end_day).isocalendar()[1]
    # Gets the total number of weeks in the current month.
    total_weeks = 1 + end_week_number - start_week_number

    final_form = {}  # final_form variable.

    def get_current_weeks_total_amount(week_number, week_data):
        """
        A utility function that populates the final_form dictionary with
        key as week_number_string and value as the total sum of amount of
        expenses per week from Expense Model.
        """

        # Creates string with given week number.
        week_number_string = f"Week {week_number+1}"
        # Checks if week_data is not empty.
        if week_data:
            # For loop that iterates over week_data.
            for item in week_data:
                # Checks if current week_number_string is not in
                # the final_form dictionary.
                if week_number_string not in final_form:
                    # Then adds that week_number_string as key and
                    # with a value of 0.
                    final_form[week_number_string] = 0
                # Else adds the current items amount to the value of
                # current week_number_string
                final_form[week_number_string] += item.amount

    # For loop that iterates over total_weeks.
    for week_number in range(total_weeks):
        # Gets the current weeks data.
        week_data = expenses.filter(date__week=start_week_number + week_number)
        # Calls helper function to populate that key with value.
        get_current_weeks_total_amount(week_number, week_data)
    # Return JsonResponse with required data.
    return JsonResponse({'expense_weekly_data': final_form}, safe=False)
