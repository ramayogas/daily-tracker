from datetime import datetime

from models import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    urgency = db.Column(
        db.String(20),
        default="Medium"
    )

    due_date = db.Column(
        db.DateTime,
        nullable=True
    )

    note = db.Column(
        db.Text,
        nullable=True
    )

    is_done = db.Column(
        db.Boolean,
        default=False
    )

    archived = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    task_type = db.Column(
        db.String(20),
        default="one_time"
    )
    
    custom_type = db.Column(
    db.String(20),
    nullable=True
    )   

    custom_value = db.Column(
        db.Integer,
        nullable=True
    )
        
    repeat_days = db.Column(
        db.String(100),
        nullable=True
    )

    def __repr__(self):
        return f"<Task {self.title}>"