from datetime import datetime
import calendar
from flask import request

from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from models.task import Task

calendar_bp = Blueprint(
    "calendar",
    __name__
)

@calendar_bp.route("/calendar")
@login_required
def calendar_view():

    today = datetime.today()
    year = int(
        request.args.get(
            "year",
            today.year
        )
    )
    month = int(
        request.args.get(
            "month",
            today.month
        )
    )
    tasks = Task.query.filter_by(
        user_id=current_user.id,
        archived=False
    ).all()

    month_calendar = calendar.monthcalendar(
        year,
        month
    )

    tasks_json = [
        {
            "id": task.id,
            "title": task.title,
            "date": task.due_date.strftime(
                "%Y-%m-%d"
            )
        }
        for task in tasks
        if task.due_date
    ]
    return render_template(
        "calendar.html",
        month_calendar=month_calendar,
        year=year,
        month=month,
        tasks=tasks,
        tasks_json=tasks_json
    )
