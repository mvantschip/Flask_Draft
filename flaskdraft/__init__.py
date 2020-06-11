from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flaskdraft.config import Config
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from flaskdraft.bids.routes import bids
    from flaskdraft.main.routes import main
    from flaskdraft.search.routes import search
    from flaskdraft.errors.handlers import errors
    from flaskdraft.users.routes import users
    app.register_blueprint(bids)
    app.register_blueprint(main)
    app.register_blueprint(search)
    app.register_blueprint(errors)
    app.register_blueprint(users)

    with app.app_context():
        db.create_all()

    return app
