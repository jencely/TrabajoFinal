from flask import Flask
from config import Config
from app.models import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos
    init_db()

    # Registrar el Blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app
