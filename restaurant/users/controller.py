from flask import Blueprint
from .service import change_password_service,login_service,signup_khach_hang_service
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt
from flask import request,jsonify


users = Blueprint("users",__name__)

revoked_tokens = set()
def get_revoked_token():
    return revoked_tokens

@users.route('/api/login-user',methods= ['POST'])
def login_user():
    return login_service()

@users.route('/api/sigup-user/khach-hang',methods=['POST'])
def signup_user_khach_hang():
    return signup_khach_hang_service()

@users.route('/api/users/change-password-user',methods = ['PUT'])
def change_password_user():
    return change_password_service()


@users.route('/api/logout-user',methods=['DELETE'])
def logout_user():
    return logout()


@jwt_required()
def logout():
    jwt = get_jwt()
    
    jti = jwt['jti']
    revoked_tokens = get_revoked_token()
    revoked_tokens.add(jti)
    return jsonify({"message": "Logout successful"}), 200