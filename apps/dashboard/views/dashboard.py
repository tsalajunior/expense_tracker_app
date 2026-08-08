from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from apps.expenses.models import Expense


@login_required
def index(request):

    today = timezone.localdate()

    first_day_of_month = today.replace(day=1)

    expenses = Expense.objects.filter(
        user=request.user
    ).select_related(
        "category",
        "payment_method",
    )

    today_expenses = expenses.filter(
        expense_date=today
    )

    month_expenses = expenses.filter(
        expense_date__gte=first_day_of_month,
        expense_date__lte=today,
    )

    context = {
        "page_title": "Dashboard",

        "today_expenses_total": (
            today_expenses.aggregate(
                total=Sum("amount")
            )["total"] or 0
        ),

        "month_expenses_total": (
            month_expenses.aggregate(
                total=Sum("amount")
            )["total"] or 0
        ),

        "month_expenses_count": month_expenses.count(),

        "recent_expenses": expenses[:5],
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )