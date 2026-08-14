from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from itertools import chain

from apps.expenses.models import Expense
from apps.incomes.models import Income


@login_required
def index(request):

    today = timezone.localdate()

    first_day_of_month = today.replace(day=1)

    # ==========================================================
    # EXPENSES
    # ==========================================================

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

    # ==========================================================
    # INCOMES
    # ==========================================================

    incomes = Income.objects.filter(
        user=request.user
    ).select_related(
        "category",
    )

    today_incomes = incomes.filter(
        income_date=today
    )

    month_incomes = incomes.filter(
        income_date__gte=first_day_of_month,
        income_date__lte=today,
    )

    # ==========================================================
    # TOTALS
    # ==========================================================

    today_expenses_total = (
        today_expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    month_expenses_total = (
        month_expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    today_incomes_total = (
        today_incomes.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    month_incomes_total = (
        month_incomes.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    # ==========================================================
    # RECENT TRANSACTIONS
    # ==========================================================

    recent_expenses = expenses.select_related(
        "category",
    )[:5]

    recent_incomes = incomes.select_related(
        "category",
    )[:5]

    recent_transactions = sorted(
        chain(recent_expenses, recent_incomes),
        key=lambda transaction: transaction.expense_date
        if hasattr(transaction, "expense_date")
        else transaction.income_date,
        reverse=True,
    )[:5]


    # ==========================================================
    # BALANCE & SAVINGS
    # ==========================================================

    current_balance = (
        month_incomes_total - month_expenses_total
    )

    # monthly_savings = current_balance

    # ==========================================================
    # CONTEXT
    # ==========================================================

    context = {
        "page_title": "Dashboard",

        "today_expenses_total": today_expenses_total,
        "month_expenses_total": month_expenses_total,

        "today_incomes_total": today_incomes_total,
        "month_incomes_total": month_incomes_total,

        "current_balance": current_balance,

        "month_expenses_count": month_expenses.count(),

        "recent_transactions": recent_transactions,
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )