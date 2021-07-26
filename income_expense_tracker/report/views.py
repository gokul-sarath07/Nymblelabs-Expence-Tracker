from django.shortcuts import render
from expenses.models import Expense
import datetime
import calendar
from django.http import JsonResponse
from django.db.models.functions import ExtractWeek


def stats_view(request):
    return render(request, 'report/index.html')

def get_current_month_start_and_end_date():
    todays_date = datetime.date.today()
    year, month, day = str(todays_date).split('-')
    _, last_day_of_month = calendar.monthrange(int(year), int(month))
    start_date = datetime.date(int(year), int(month), 1)
    end_date = datetime.date(int(year), int(month), last_day_of_month)
    return start_date, end_date

def category_summery(request):
    start_date, end_date = get_current_month_start_and_end_date()
    expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date, owner=request.user).order_by('-date')
    final_form = {}

    def get_category(expense):
        return expense.category

    def get_category_amount(category):
        amount = 0
        filter_expenses_by_category = expenses.filter(category=category)
        for item in filter_expenses_by_category:
            amount += item.amount
        return amount

    category_list = list(set(map(get_category, expenses)))
    for category in category_list:
        final_form[category] = get_category_amount(category)

    return JsonResponse({'expense_category_data': final_form}, safe=False)


def weekly_summery(request):
    start_date, end_date = get_current_month_start_and_end_date()
    expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date, owner=request.user).order_by('-date')

    start_year, start_month, start_day = map(int, str(start_date).split('-'))
    end_year, end_month, end_day = map(int, str(end_date).split('-'))

    start_week_number = datetime.date(start_year, start_month, start_day).isocalendar()[1]
    end_week_number = datetime.date(end_year, end_month, end_day).isocalendar()[1]
    total_weeks = 1 + end_week_number - start_week_number

    final_form = {}

    def get_current_weeks_total_amount(week_number, week_data):
        week_string = f"Week {week_number+1}"
        if week_data:
            for item in week_data:
                if week_string not in final_form:
                    final_form[week_string] = 0
                final_form[week_string] += item.amount


    for week_number in range(total_weeks):
        week_data = expenses.filter(date__week=start_week_number + week_number)
        get_current_weeks_total_amount(week_number, week_data)

    return JsonResponse({'expense_weekly_data': final_form}, safe=False)
