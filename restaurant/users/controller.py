from flask import Blueprint
from .service import change_password_service,login_service,signup_khach_hang_service
users = Blueprint("users",__name__)

@users.route('/api/login-user',methods= ['POST'])
def login_user():
    return login_service()

@users.route('/api/sigup-user/khach-hang',methods=['POST'])
def signup_user_khach_hang():
    return signup_khach_hang_service()

@users.route('/api/users/change-password-user',methods = ['PUT'])
def change_password_user():
    return change_password_service()
