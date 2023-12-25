from restaurant.extension import db
from restaurant.restaurant_ma import UsersChema
from restaurant.models import Users,Nhanvien,Khachhang
from flask import request,jsonify
from sqlalchemy import func
import json
from werkzeug.security import generate_password_hash,check_password_hash

user_schema = UsersChema()
users_schema = UsersChema(many=True)

def signup_khach_hang_service():
    data = request.json
    if data and ('user_name' in data) and ('email' in data) and ('password' in data) and ('hoten' in data):
        user_name = data['user_name']
        email = data['email']
        role = 'Khach Hang'
        password = data['password']
        hoten = data['hoten']
        doanhthu = 0
        diemtichluy = 0
        user_check = Users.query.filter_by(user_name=user_name).first()
        if user_check:
            return jsonify({"message":"user_name exist!"})
        else:
            try:
                password = generate_password_hash(password)
                user = Users(user_name=user_name,password=password,email=email,role=role)
                db.session.add(user)
                db.session.commit()
            except IndentationError:
                db.session.rollback()
                return jsonify({"message":"Can't create user!"})
            try:
                max_ma_kh = db.session.query(func.max(Khachhang.ma_kh)).scalar()
                ma_kh = max_ma_kh + 1 if max_ma_kh is not None else 1
                khach_hang = Khachhang(ma_kh=ma_kh,hoten=hoten,user_name=user_name,diemtichluy=diemtichluy,doanhthu=doanhthu)
                db.session.add(khach_hang) 
                db.session.commit()
                return jsonify({"message":"SignUp Success!"})
            except IndentationError:
                db.session.rollback()
                return jsonify({"message":"Can't create infor user!"})
    else:
        return jsonify({"message": "Request Error!"})   
    

def login_service():
    data = request.json
    try :
        user_name = data['user_name']
        password = data['password']
    except KeyError:
        return jsonify({"message": "Request error! Missing user_name or password."})
    
    if data and ('user_name' in data) and ('password' in data) :
        user = Users.query.filter_by(user_name = user_name).first()
        if user:
            role = user.role
            if check_password_hash(user.password,password) :
                return jsonify({"message" : "Login Access!"},{"role": f"{role}"})
            else:
                return jsonify({"message" : "Password error!"})
        else:
            return jsonify({"message" : "Not found user"})
    else:
        return jsonify({"message" : "Request error!"})

def change_password_service():
    data = request.json
    if data and ('user_name' in data) and ('password' in data) :
        user_name = data['user_name']
        password = data['password']
        password_new = data['password_new']
        user = Users.query.filter_by(user_name = user_name).first()
        password_new = generate_password_hash(password=password_new)
        
        if user :
            if check_password_hash(user.password,password) :
                try:
                    user.password = password_new
                    db.session.commit()
                    return jsonify({"message" : "Change Access!"})
                except IndentationError:
                    db.session.rollback()
                    return jsonify({"message":"Can't change password!"})
            else:
                return jsonify({"message" : "Password Incorrect!"})
        else:
            return jsonify({"message" : "Not found user!"})   
    else :
        return jsonify({"message" : "Request Eror!"}) 