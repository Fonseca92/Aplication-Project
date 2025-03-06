from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_session import Session
from config import Config
import logging

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    Session(app)
    
    from app import routes, views
    app.register_blueprint(routes.bp)
    app.register_blueprint(views.views_bp)
    
    # Logging setup
    logging.basicConfig(filename='app.log', level=logging.INFO)
    
    return app