from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import IMAGES, UploadSet, configure_uploads


login_manager = LoginManager()
bootstrap = Bootstrap()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_options[config_name])

    # flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # register blueprints
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    configure_uploads(app, photos)



    return app