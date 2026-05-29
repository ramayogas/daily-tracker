from flask import Flask
from flask_login import login_required

from config import Config
from models import db, login_manager

# import model
from models.user import User
from models.category import Category
from models.task import Task

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.category import category_bp
    from routes.task import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(task_bp)

    # create database
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)