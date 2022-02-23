from flask import Flask
from app.routes.user_route import bp_user

def init_app(app: Flask) -> None:
    app.register_blueprint(bp_user)