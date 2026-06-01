from flask import Flask
from flask_login import login_required

from config import Config
from models import db, login_manager

# import model
from models.user import User
from models.category import Category
from models.task import Task
from datetime import datetime
from routes.calendar import calendar_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @app.template_filter("pretty_days")
    def pretty_days(days):
        mapping = {
            "mon": "Monday",
            "tue": "Tuesday",
            "wed": "Wednesday",
            "thu": "Thursday",
            "fri": "Friday",
            "sat": "Saturday",
            "sun": "Sunday"
        }

        if not days:
            return ""

        return ", ".join(
            mapping.get(day.strip(), day)
            for day in days.split(",")
        )

    # register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.category import category_bp
    from routes.task import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(calendar_bp)

    # create database
    with app.app_context():
        db.create_all()

    return app


app = create_app()

@app.context_processor
def inject_now():
    return {
        "now": datetime.now()
    }

if __name__ == "__main__":
    app.run(debug=True)
    
