from restaurant.extension import db
from restaurant.restaurant_ma import KhachhangChema
from restaurant.models import Users,Nhanvien,Khachhang,Ban
from flask import request,jsonify
from sqlalchemy import func
import json
from flask_jwt_extended import jwt_required,current_user

Khachhang_schema = KhachhangChema()
Khachhangs_schema = KhachhangChema(many=True)

@jwt_required()
def get_info_khach_hang():
    user = Khachhang.query.filter_by(user_name=current_user.user_name).first()
    if user :
        return Khachhang_schema.jsonify(user),200
    else:
        return jsonify({"message":"Not found user!"}),400

@jwt_required()
def update_hoten():
    user = Khachhang.query.filter_by(user_name=current_user.user_name).first()
    if user :
        data = request.json
        if data and ('hoten' in data):
            hoten_new = request.json['hoten']
            try:
                user.hoten = hoten_new
                db.session.commit()
                return jsonify({"message":"Update Access!"}),200
            except IndentationError:
                db.session.rollback()
                return jsonify({"message":"Can't Update!"}),409
        else:
            return jsonify({"message":"Not found User!"}),400
    else:
        return jsonify({"message":"Not found user!"}),400
        
@jwt_required()
def book_seat(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        if ban.tinhtrang == 'Con trong':
            try:
                ban.tinhtrang = 'Da dat truoc'
                db.session.commit()
                return jsonify({"message":"Booking Access!"}),200
            except Exception:
                db.session.rollback()
                return jsonify({"message":"Can't Booking!"}),409
        else:
            return jsonify({"message":"Can't Booking!"}),409
    else:
        return jsonify({"message":"Not found Table!"}),400


@jwt_required()
def cancel_book_seat(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        if ban.tinhtrang == 'Da dat truoc':
            try:
                ban.tinhtrang = 'Con trong'
                db.session.commit()
                return jsonify({"message":"Access!"}),200
            except Exception:
                db.session.rollback()
                return jsonify({"message":"Cancle Booking Error!"}),409
        else:
            return jsonify({"message":"Cancle Booking Error!"}),409
    else:
        return jsonify({"message":"Not found Table!"}),400
    

@jwt_required()
def get_makh_by_user_name(user_name):
    user = Khachhang.query.filter_by(user_name=user_name).first()
    if user:
        return jsonify({"message": f"{user.ma_kh}"}),200
    else:
        return jsonify({"message":"Not found user!"}),404
