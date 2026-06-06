from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from models.task import Task
from utils.calendar import get_month_days, get_tasks_for_date
from utils.recurring import is_completed_on


calendar_bp = Blueprint("calendar", __name__)


@calendar_bp.route("/calendar")
@login_required
def calendar():

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    from datetime import date

    today = date.today()

    if not year:
        year = today.year
    if not month:
        month = today.month

    all_tasks = Task.query.filter_by(
        user_id=current_user.id,
        archived=False
    ).all()

    days = get_month_days(year, month)

    selected_date = request.args.get("date")

    selected_tasks = []

    if selected_date:
        from datetime import datetime

        selected_date = datetime.strptime(
            selected_date,
            "%Y-%m-%d"
        ).date()

        selected_tasks = get_tasks_for_date(
            all_tasks,
            selected_date
        )

    calendar_data = []

    for d in days:
        tasks = get_tasks_for_date(all_tasks, d)

        calendar_data.append({
            "date": d,
            "count": len(tasks)
        })

    return render_template(
        "calendar.html",
        calendar_data=calendar_data,
        selected_tasks=selected_tasks,
        selected_date=selected_date,
        year=year,
        month=month,
        is_completed_on=is_completed_on
    )
    
