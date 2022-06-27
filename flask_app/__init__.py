from flask import Flask
from flask_app.main.main_routes import main_bp
from flask_app.main.submit_routes import submit_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(submit_bp)

    @app.route('/')
    def index():
        return 'start', 200

    return app

