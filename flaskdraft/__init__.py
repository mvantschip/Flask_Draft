from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskdraft.config import Config

db = SQLAlchemy()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from flaskdraft.bids.routes import bids
    from flaskdraft.main.routes import main
    from flaskdraft.search.routes import search
    from flaskdraft.errors.handlers import errors
    app.register_blueprint(bids)
    app.register_blueprint(main)
    app.register_blueprint(search)
    app.register_blueprint(errors)

    return app
