from flask import Flask
from app.db_connect import close_db
from app.blueprints.projects import projects_bp
from app.blueprints.tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

    # Register blueprints
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)

    # Register teardown function
    app.teardown_appcontext(close_db)

    return app