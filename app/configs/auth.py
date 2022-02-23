from flask_httpauth import HTTPTokenAuth
from app.models.user_model import User

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    return user