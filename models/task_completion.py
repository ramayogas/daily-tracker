from datetime import datetime
from models import db


class TaskCompletion(db.Model):
    __tablename__ = "task_completions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )

    completion_date = db.Column(
        db.Date,
        nullable=False
    )

    completed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<TaskCompletion task={self.task_id} date={self.completion_date}>"
