from flask import Flask


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    if config_overrides:
        app.config.update(config_overrides)

    from todo.models import db
    from todo.models.todo import Todo

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from todo.views.routes import api
    app.register_blueprint(api)

    return app
