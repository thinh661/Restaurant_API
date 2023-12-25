from restaurant.extension import db
from restaurant.restaurant_ma import KhachhangChema,NhanvienSchema,UsersChema,BanSchema,HoadonSchema
from restaurant.models import Users,Nhanvien,Khachhang,Ban,Hoadon
from flask import request,jsonify
from sqlalchemy.sql import func
import json

Nhanvien_schema = NhanvienSchema()
Nhanviens_schema = NhanvienSchema(many=True)
Ban_schema = BanSchema()
Bans_schema = BanSchema(many=True)

def get_all_staff():
    all_staff = Nhanvien.query.all()
    if all_staff :
        return Nhanviens_schema.jsonify(all_staff)
    else:
        return jsonify({"message":"Not found staff!"})

def get_staff_by_name(name):
    staff = Nhanvien.query.filter(func.lower(Nhanvien.hoten) == func.lower(name)).first()
    if staff is not None:
        return Nhanvien_schema.jsonify(staff)
    else:
            return jsonify({"message":"Not found staff!"})

def add_staff():
    data = request.json
    user_name = data['user_name']
    email = data['email']
    role = data['role']
    password = data['password']
    hoten = data['hoten']
    chucvu = data['chucvu']
    sdt = data['sdt']
    
    if data :
        staff_user = Users.query.filter_by(user_name=user_name).first()
        if staff_user:
            return jsonify({"message":"user_name exist!"})
        else:
            try:
                user = Users(user_name=user_name,password=password,email=email,role=role)
                db.session.add(user)
                db.session.commit()
            except IndentationError:
                db.session.rollback()
                return jsonify({"message":"Can't create user!"})
            try:
                max_ma_nv = db.session.query(func.max(Nhanvien.ma_nv)).scalar()
                ma_nv = max_ma_nv + 1 if max_ma_nv is not None else 1
                nhan_vien = Nhanvien(ma_nv=ma_nv,hoten=hoten,chucvu=chucvu,user_name=user_name,sdt=sdt)
                db.session.add(nhan_vien)
                db.session.commit()
                return jsonify({"message":"SignUp Success!"})
            except IndentationError:
                db.session.rollback()
                return jsonify({"message":"Can't create infor user!"})
    else:
        return jsonify({"message": "Request Error!"})
    

def delete_staff(ma_nv):
    try:
        user = Nhanvien.query.filter_by(ma_nv=ma_nv).first()
        if user :
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message":"Delete Access!"})
        else:
            return jsonify({"message" : "Not found staff!"})
    except IndentationError:
            db.session.rollback()
            return jsonify({"message":"Can't Delete Staff!"})
        

def fix_staff(ma_nv: int):
    data = request.json
    staff = Nhanvien.query.filter_by(ma_nv=ma_nv).first()

    if staff:
        try:
            if 'hoten' in data and data['hoten'] is not None:
                staff.hoten = data['hoten']
            if 'chucvu' in data and data['chucvu'] is not None:
                staff.chucvu = data['chucvu']
            if 'sdt' in data and data['sdt'] is not None:
                staff.sdt = data['sdt']
            
            db.session.commit()
            return jsonify({"message": "Update Access!"})
        except Exception:
            db.session.rollback()
            return jsonify({"message": "Request Error!"})
    else:
        return jsonify({"message": "Not found staff!"})
    

def add_table():
    data = request.json
    if data and ('ten_ban' in data) and ('vitri' in data) and ('soghe' in data) :
        ten_ban = data['ten_ban']
        vitri = data['vitri']
        soghe = data['soghe']
        max_ma_ban = db.session.query(func.max(Ban.ma_ban)).scalar()
        ma_ban = max_ma_ban + 1 if max_ma_ban is not None else 1
        check_ban = Ban.query.filter(func.lower(Ban.ten_ban) == func.lower(ten_ban)).first()
        if check_ban:
            return jsonify({"message":"Name of table is exist!"})
        else:
            try:
                ban = Ban(ma_ban=ma_ban,ten_ban=ten_ban,vitri=vitri,soghe=soghe)
                db.session.add(ban)
                db.session.commit()
                return jsonify({"message":"Add Table Access!"})
            except Exception:
                db.session.rollback()
                return jsonify({"message":"Can't Add Table!"})
    else:
        return jsonify({"message":"Request Error!"})

def delete_table(ma_ban):
    ban = Ban.query.filter_by(ma_ban=ma_ban).first()
    if ban:
        try:
            db.session.delete(ban)
            db.session.commit()
            return jsonify({"message":"Delete Table Access!"})
        except Exception as e :
            db.session.rollback()
            return jsonify({"message":f"Error : {e}"})
    else:
        return jsonify({"message":"Not found Table!"})

def get_all_table():
    all_ban = Ban.query.all()
    if all_ban:
        return Bans_schema.jsonify(all_ban)
    else:
        return jsonify({"message" : "Not found Table!"})
    
def get_table_by_name(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        return Ban_schema.jsonify(ban)
    else:
        return jsonify({"message":"Not found Table!"})

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

def create_bill():
    pass

def take_bill(ma_ban):
    pass

def take_detail_bill(ma_hd):
    pass

def update_bill():
    pass
