from datetime import date


def is_due_today(task):
    today = date.today()

    # ONE TIME
    if task.task_type == "one_time":
        if not task.due_date:
            return False
        return task.due_date.date() == today

    # HABIT
    elif task.task_type == "habit":
        if not task.repeat_days:
            return False
        weekday = today.strftime(
            "%a"
        ).lower()[:3]
        repeat_days = [
            d.strip()
            for d in task.repeat_days.split(",")
        ]
        return weekday in repeat_days

    # CUSTOM
    elif task.task_type == "custom":
        if (
            task.custom_type
            == "every_n_days"
        ):
            if not task.custom_value:
                return False
            days_since_creation = (
                today -
                task.created_at.date()
            ).days
            return (
                days_since_creation %
                int(task.custom_value)
                == 0
            )
        elif (
            task.custom_type
            == "day_of_month"
        ):
            return (
                today.day ==
                int(task.custom_value)
            )

    return False