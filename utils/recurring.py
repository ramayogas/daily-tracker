from datetime import date


def is_due_on(task, target_date: date):

    # ONE TIME
    if task.task_type == "one_time":
        if not task.due_date:
            return False
        return task.due_date.date() == target_date

    # HABIT
    elif task.task_type == "habit":

        if not task.repeat_days:
            return False

        weekday = target_date.strftime("%a").lower()[:3]

        repeat_days = {
            d.strip().lower()
            for d in task.repeat_days.split(",")
            if d.strip()
        }

        return weekday in repeat_days

    # CUSTOM
    elif task.task_type == "custom":

        if task.custom_type == "every_n_days":
            if not task.custom_value:
                return False

            days_since = (target_date - task.created_at.date()).days

            return days_since % int(task.custom_value) == 0

        elif task.custom_type == "day_of_month":
            if not task.custom_value:
                return False

            return target_date.day == int(task.custom_value)

    return False


def is_due_today(task):
    return is_due_on(task, date.today())