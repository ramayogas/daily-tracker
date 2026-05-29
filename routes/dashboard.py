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

    todays_pending = [
        task for task in all_tasks
        if (
            not task.is_done and
            task.due_date and
            task.due_date.date()
            == datetime.today().date()
        )
    ]

    recent_completed = sorted(
        [
            task for task in all_tasks
            if task.is_done
        ],
        key=lambda x: x.created_at,
        reverse=True
    )[:5]

    return render_template(
        "dashboard.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_rate=completion_rate,
        todays_pending=todays_pending,
        recent_completed=recent_completed
    )