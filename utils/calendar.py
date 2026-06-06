from datetime import date, timedelta
from utils.recurring import is_due_on


def get_tasks_for_date(tasks, target_date):
    return [
        task for task in tasks
        if is_due_on(task, target_date)
    ]


def get_month_days(year, month):
    first_day = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    days = []
    current = first_day

    while current < next_month:
        days.append(current)
        current += timedelta(days=1)

    return days