from restaurant.extension import db
from restaurant.restaurant_ma import KhachhangChema
from restaurant.models import Users,Nhanvien,Khachhang,Ban
from flask import request,jsonify
from sqlalchemy import func
import json

Khachhang_schema = KhachhangChema()
Khachhangs_schema = KhachhangChema(many=True)

def get_info_khach_hang(user_name):
    user = Khachhang.query.filter_by(user_name=user_name).first()
    print(user.hoten)
    if user :
        return Khachhang_schema.jsonify(user)
    else:
        return jsonify({"message":"Not found user!"})

def update_hoten(user_name):
    user = Khachhang.query.filter_by(user_name=user_name).first()
    hoten_new = request.json['hoten']
    try:
        user.hoten = hoten_new
        db.session.commit()
        return jsonify({"message":"Update Access!"})
    except IndentationError:
        db.session.rollback()
        return jsonify({"message":"Can't Update!"})
        

def book_seat(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        if ban.tinhtrang == 'Con trong':
            try:
                ban.tinhtrang = 'Da dat truoc'
                db.session.commit()
                return jsonify({"message":"Booking Access!"})
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"})
        else:
            return jsonify({"message":"Can't Booking!"})
    else:
        return jsonify({"message":"Not found Table!"})

def cancel_book_seat(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        if ban.tinhtrang == 'Da dat truoc':
            try:
                ban.tinhtrang = 'Con trong'
                db.session.commit()
                return jsonify({"message":"Access!"})
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"})
        else:
            return jsonify({"message":"Cancle Booking Error!"})
    else:
        return jsonify({"message":"Not found Table!"})
