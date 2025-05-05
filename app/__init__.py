#create app
from flask import Flask
from .config import DevelopmentConfig

'''
Factory Pattern: it first loads and builds components INSIDE the create_app before running or returning the app.
Inside imports lazy import all of the imports by referring the import. 
It delays the initialization
'''
def create_app():
    app = Flask(__name__, template_folder='blueprints/templates')
    app.config.from_object(DevelopmentConfig())

    from .extensions import db, migrate, login_manager, bcrypt #loads db, but not yet used
    db.init_app(app)                                            #uses db
    migrate.init_app(app, db)

    from .blueprints.central_models import all_models       #loads all of the models

    login_manager.init_app(app) 

    from .config import LoginManagerConfig
    LoginManagerConfig.config_login(login_manager)

    from .blueprints import all_blueprints
    for blueprint, prefix in all_blueprints:
        app.register_blueprint(blueprint=blueprint, url_prefix=prefix)

    return app