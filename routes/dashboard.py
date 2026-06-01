from datetime import datetime

from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from models.task import Task

from utils.recurring import (
    is_due_today
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    all_tasks = Task.query.filter_by(
        user_id=current_user.id,
        archived=False
    ).all()

    total_tasks = len(all_tasks)

    completed_tasks = len([
        task for task in all_tasks
        if task.is_done
    ])

    pending_tasks = len([
        task for task in all_tasks
        if not task.is_done
    ])

    completion_rate = 0

    if total_tasks > 0:
        completion_rate = round(
            (
                completed_tasks /
                total_tasks
            ) * 100
        )

    today = datetime.today().date()

    today_tasks = [
    task
    for task in all_tasks
    if (
        not task.is_done
        and is_due_today(task)
    )
]
    
    today_tasks = sorted(
        today_tasks,
        key=lambda x: x.due_date or datetime.max
    )[:5]
  
    habit_tasks = [
        task
        for task in all_tasks
        if (
            task.task_type == "habit"
            and not task.is_done
            and is_due_today(task)
        )
    ][:5]
    
    recent_completed = sorted(
        [
            task for task in all_tasks
            if task.is_done
        ],
        key=lambda x: x.created_at,
        reverse=True
    )[:5]
    
    custom_tasks = [
        task for task in all_tasks
        if (
            task.task_type == "custom"
            and not task.is_done
        )
    ]

    return render_template(
    "dashboard.html",
    total_tasks=total_tasks,
    completed_tasks=completed_tasks,
    pending_tasks=pending_tasks,
    completion_rate=completion_rate,
    today_tasks=today_tasks,
    habit_tasks=habit_tasks,
    custom_tasks=custom_tasks,
    recent_completed=recent_completed
)