from datetime import date
from models.task_completion import TaskCompletion


def is_completed_on(task, target_date: date):
    """Check if task is completed on a specific date"""
    if task.task_type == "one_time":
        # For one-time tasks, check is_done flag
        return task.is_done
    else:
        # For recurring tasks, check TaskCompletion records
        completion = TaskCompletion.query.filter_by(
            task_id=task.id,
            completion_date=target_date
        ).first()
        return completion is not None


def is_due_on(task, target_date: date):

    # ONE TIME
    if task.task_type == "one_time":
        if not task.due_date:
            return False
        task_date = task.due_date.date() == target_date
        
        # Check if this one-time task is marked as done
        if task_date and task.is_done:
            return False
            
        return task_date

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

        is_due = weekday in repeat_days
        
        # For recurring tasks, check if this specific instance is completed
        if is_due:
            return not is_completed_on(task, target_date)
            
        return False

    # CUSTOM
    elif task.task_type == "custom":

        if task.custom_type == "every_n_days":
            if not task.custom_value:
                return False

            days_since = (target_date - task.created_at.date()).days
            is_due = days_since % int(task.custom_value) == 0
            
            # For recurring tasks, check if this specific instance is completed
            if is_due:
                return not is_completed_on(task, target_date)
                
            return False

        elif task.custom_type == "day_of_month":
            if not task.custom_value:
                return False

            is_due = target_date.day == int(task.custom_value)
            
            # For recurring tasks, check if this specific instance is completed
            if is_due:
                return not is_completed_on(task, target_date)
                
            return False

    return False


def is_due_today(task):
    return is_due_on(task, date.today())