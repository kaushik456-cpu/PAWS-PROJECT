from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
admin = Admin()
limiter = Limiter(key_func=get_remote_address)
swagger = Swagger()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    admin.init_app(app)
    CORS(app)
    limiter.init_app(app)
    swagger.init_app(app)
    
    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.reports import reports_bp
    from app.routes.users import users_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Register admin views
    from app.admin_panel.views import setup_admin
    setup_admin(admin, db)
    
    return app
