from flask import Blueprint
from app.controllers import user_controller

bp_user = Blueprint('bp_user', __name__, url_prefix='/api')

bp_user.get('')(user_controller.get_user)
bp_user.put('')(user_controller.put_user)
bp_user.delete('')(user_controller.delete_user)
bp_user.post('/signup')(user_controller.create_user)
bp_user.post('/signin')(user_controller.login)