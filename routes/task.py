from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models import task
from models.task import Task
from models.category import Category


task_bp = Blueprint(
    "task",
    __name__
)


@task_bp.route("/tasks")
@login_required
def tasks():
    task_type = request.args.get(
        "task_type",
        "all"
    )
    search = request.args.get(
        "search",
        ""
    )

    status = request.args.get(
        "status",
        "all"
    )

    urgency = request.args.get(
        "urgency",
        "all"
    )

    category_id = request.args.get(
        "category",
        "all"
    )

    query = Task.query.filter_by(
        user_id=current_user.id,
        archived=False
    )

    # Search
    if search:

        query = query.filter(
            Task.title.ilike(
                f"%{search}%"
            )
        )

    # Status
    if status == "done":

        query = query.filter_by(
            is_done=True
        )

    elif status == "pending":

        query = query.filter_by(
            is_done=False
        )

    # Urgency
    if urgency != "all":

        query = query.filter_by(
            urgency=urgency
        )

    # Category
    if category_id != "all":

        query = query.filter_by(
            category_id=category_id
        )

    tasks = query.order_by(
        Task.created_at.desc()
    ).all()

    categories = Category.query.filter_by(
        user_id=current_user.id,
        archived=False
    ).all()
    
    if task_type != "all":

        query = query.filter_by(
            task_type=task_type
        )

    return render_template(
        "tasks.html",
        tasks=tasks,
        categories=categories,
        search=search,
        status=status,
        urgency=urgency,
        selected_category=category_id,
        task_type=task_type
    )

@task_bp.route(
    "/tasks/add",
    methods=["POST"]
)
@login_required
def add_task():

    title = request.form.get(
        "title"
    )

    category_id = request.form.get(
        "category_id"
    )

    urgency = request.form.get(
        "urgency"
    )

    due_date_raw = request.form.get("due_date")

    if due_date_raw:
        due_date = datetime.strptime(
            due_date_raw,
            "%Y-%m-%dT%H:%M"
        )
    else:
        due_date = None

    note = request.form.get(
        "note"
    )
    
    task_type = request.form.get(
    "task_type"
    )

    custom_type = request.form.get(
    "custom_type"
    )

    custom_value = request.form.get(
        "custom_value"
    )

    repeat_days = request.form.getlist(
        "repeat_days"
    )


    new_task = Task(
        title=title,
        user_id=current_user.id,
        category_id=category_id,
        urgency=urgency,
        due_date=due_date,
        note=note,
        task_type=task_type,
         repeat_days=", ".join(repeat_days)
        if repeat_days
        else None,

        custom_type=custom_type
        if custom_type
        else None,

        custom_value=int(custom_value)
        if custom_value
        else None
        )

    db.session.add(new_task)
    db.session.commit()

    flash(
        "Task added.",
        "success"
    )

    return redirect(
        url_for("task.tasks")
    )


@task_bp.route(
    "/tasks/archive/<int:id>"
)
@login_required
def archive_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    task.archived = True

    db.session.commit()

    flash(
        "Task archived.",
        "success"
    )

    return redirect(
        url_for("task.tasks")
    )
@login_required
def delete_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash(
        "Task deleted.",
        "success"
    )

    return redirect(
        url_for("task.tasks")
    )
@task_bp.route(
    "/tasks/toggle/<int:id>"
)
@login_required
def toggle_task(id):
    from datetime import date
    from models.task_completion import TaskCompletion

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    today = date.today()
    
    # For recurring tasks (habit, custom), track completions by date
    if task.task_type in ["habit", "custom"]:
        existing_completion = TaskCompletion.query.filter_by(
            task_id=task.id,
            completion_date=today
        ).first()
        
        if existing_completion:
            # Mark as incomplete by removing the completion record
            db.session.delete(existing_completion)
        else:
            # Mark as complete for today
            completion = TaskCompletion(
                task_id=task.id,
                completion_date=today
            )
            db.session.add(completion)
    else:
        # For one-time tasks, use the is_done flag
        task.is_done = not task.is_done
        if task.is_done:
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None

    db.session.commit()

    next_page = request.args.get(
    "next"
    )

    if next_page == "dashboard":
        return redirect(
            url_for("dashboard.dashboard")
        )

    return redirect(
        url_for("task.tasks")
    )
@task_bp.route(
    "/tasks/edit/<int:id>",
    methods=["GET", "POST"]
)

@login_required
def edit_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    categories = Category.query.filter_by(
        user_id=current_user.id,
        archived=False
    ).all()

    if request.method == "POST":
        task.task_type = request.form.get(
            "task_type"
        )

        task.repeat_days = ", ".join(
            request.form.getlist("repeat_days")
        )

        task.custom_type = request.form.get(
            "custom_type"
        )

        task.custom_value = request.form.get(
            "custom_value"
        )
        task.title = request.form.get(
            "title"
        )
        category_id = request.form.get(
            "category_id"
        )
        task.category_id = (
            category_id
            if category_id
            else None
        )
        task.urgency = request.form.get(
            "urgency"
        )
        due_date = request.form.get(
            "due_date"
        )
        task.note = request.form.get(
            "note"
        )

        if due_date:
            task.due_date = (
                datetime.strptime(
                    due_date,
                    "%Y-%m-%dT%H:%M"
                )
            )

        else:
            task.due_date = None
        db.session.commit()
        flash(
            "Task updated.",
            "success"
        )
        return redirect(
            url_for("task.tasks")
        )

    
    return render_template(
        "edit_task.html",
        task=task,
        categories=categories
    )
    