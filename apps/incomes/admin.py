from django.contrib import admin

from apps.incomes.models import Income, IncomeCategory


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "icon",
        "color",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "amount",
        "income_date",
    )

    list_filter = (
        "category",
        "income_date",
    )

    search_fields = (
        "title",
        "user__email",
    )