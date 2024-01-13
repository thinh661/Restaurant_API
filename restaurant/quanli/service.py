from restaurant.extension import db
from restaurant.restaurant_ma import KhachhangChema,NhanvienSchema,UsersChema,BanSchema,HoadonSchema,MonanSchema,VoucherSchema,ThucdonSchema
from restaurant.models import Users,Nhanvien,Khachhang,Ban,Hoadon,Thucdon,Monan,Voucher
from flask import request,jsonify
from sqlalchemy.sql import func
import json
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,current_user


Nhanvien_schema = NhanvienSchema()
Nhanviens_schema = NhanvienSchema(many=True)
Ban_schema = BanSchema()
Bans_schema = BanSchema(many=True)
Monan_schema = MonanSchema()
Monans_schema = MonanSchema(many=True)
Voucher_schema = VoucherSchema()
Vouchers_schema = VoucherSchema(many=True)
Thucdons_schema = ThucdonSchema(many=True)


# Quản lí nhân viên
@jwt_required()
def get_all_staff():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    all_staff = Nhanvien.query.all()
    if all_staff :
        return Nhanviens_schema.jsonify(all_staff),200
    else:
        return jsonify({"message":"Not found staff!"}),400

@jwt_required()
def get_staff_by_name(name):
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    staff = Nhanvien.query.filter(func.lower(Nhanvien.hoten) == func.lower(name)).first()
    if staff is not None:
        return Nhanvien_schema.jsonify(staff),200
    else:
        return jsonify({"message":"Not found staff!"}),400

@jwt_required()
def add_staff():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    hoten = data['hoten']
    chucvu = data['chucvu']
    sdt = data['sdt']
    if data :
        try:
            max_ma_nv = db.session.query(func.max(Nhanvien.ma_nv)).scalar()
            ma_nv = max_ma_nv + 1 if max_ma_nv is not None else 1
            nhan_vien = Nhanvien(ma_nv=ma_nv,hoten=hoten,chucvu=chucvu,sdt=sdt)
            db.session.add(nhan_vien)
            db.session.commit()
            return jsonify({"message":"SignUp Success!"}),201
        except IndentationError:
            db.session.rollback()
            return jsonify({"message":"Can't create infor user!"}),409
    else:
        return jsonify({"message": "Request Error!"}),400
    

@jwt_required()
def delete_staff(ma_nv):
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    try:
        user = Nhanvien.query.filter_by(ma_nv=ma_nv).first()
        if user :
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message":"Delete Access!"}),200
        else:
            return jsonify({"message" : "Not found staff!"}),409
    except IndentationError:
            db.session.rollback()
            return jsonify({"message":"Can't Delete Staff!"}),409
        

@jwt_required()
def fix_staff(ma_nv: int):
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
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
            return jsonify({"message": "Update Access!"}),200
        except Exception:
            db.session.rollback()
            return jsonify({"message": "Request Error!"}),400
    else:
        return jsonify({"message": "Not found staff!"}),400
    

# Quản lí bàn 

@jwt_required()
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
            return jsonify({"message":"Name of table is exist!"}),400
        else:
            try:
                ban = Ban(ma_ban=ma_ban,ten_ban=ten_ban,vitri=vitri,soghe=soghe)
                db.session.add(ban)
                db.session.commit()
                return jsonify({"message":"Add Table Access!"}),201
            except Exception:
                db.session.rollback()
                return jsonify({"message":"Can't Add Table!"}),409
    else:
        return jsonify({"message":"Request Error!"}),400

@jwt_required()
def delete_table(ma_ban):
    ban = Ban.query.filter_by(ma_ban=ma_ban).first()
    if ban:
        try:
            db.session.delete(ban)
            db.session.commit()
            return jsonify({"message":"Delete Table Access!"}),200
        except Exception:
            db.session.rollback()
            return jsonify({"message":"Can't delete"}),409
    else:
        return jsonify({"message":"Not found Table!"}),400


def get_all_table():
    all_ban = Ban.query.all()
    if all_ban:
        return Bans_schema.jsonify(all_ban),200
    else:
        return jsonify({"message" : "Not found Table!"}),400


def get_table_by_name(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        return Ban_schema.jsonify(ban),200
    else:
        return jsonify({"message":"Not found Table!"}),400

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
def finish_table(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        if ban.tinhtrang == 'Dang dung bua':
            try:
                ban.tinhtrang = 'Con trong'
                db.session.commit()
                return jsonify({"message":"Booking Access!"}),200
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"}),409
        else:
            return jsonify({"message":"Can't Finish!"}),409
    else:
        return jsonify({"message":"Not found Table!"}),400
  
@jwt_required()  
def start_table(ten_ban):
    ban = Ban.query.filter_by(ten_ban=ten_ban).first()
    if ban:
        if ban.tinhtrang == 'Con trong' or 'Da dat truoc':
            try:
                ban.tinhtrang = 'Dang dung bua'
                db.session.commit()
                return jsonify({"message":"Booking Access!"}),200
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"}),409
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

# Quản lí thực đơn 

@jwt_required()
def add_thuc_don():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if data :
        if "ten_td" in data :
            ten_td = data['ten_td']
        else:
            return jsonify({"message":"Request Error!"}),400
        if "mo_ta" in data :
            mo_ta = data['mo_ta']
        else:
            return jsonify({"message":"Request Error!"}),400
        
        check_td = Thucdon.query.filter_by(ten_td=ten_td).first()
        if check_td :
            return jsonify({"message" : "ten_td exist!"}),409
        max_ma_td = db.session.query(func.max(Thucdon.ma_td)).scalar()
        ma_td = int(max_ma_td) + 1 if max_ma_td is not None else 1
        thuc_don = Thucdon(ma_td=ma_td,ten_td=ten_td,mo_ta=mo_ta)
        try:
            db.session.add(thuc_don)
            db.session.commit()
        except Exception as e :
            db.session.rollback()
            return jsonify({"message":f"Error : {e}"}),409
        return jsonify({"message" : "Created!"}),201
    else :
        return jsonify({"message":"Request Error!"}),400
    



def get_all_thucdon():
    all_thucdon = Thucdon.query.all()
    if all_thucdon:
        return Thucdons_schema.jsonify(all_thucdon),200
    else:
        return jsonify({"message":"Not found!"}),404
    
def get_ten_thucdon_by_ma_td(ma_td):
    thucdon = Thucdon.query.filter_by(ma_td=ma_td).first()
    if thucdon:
        return jsonify({"ten_td":thucdon.ten_td}),200
    else:
        return jsonify({"message":"Not found!"}),404
    
def get_all_monan_by_ma_td(ma_td):
    monans = Monan.query.filter_by(ma_td=ma_td).all()
    if monans:
        return Monans_schema.jsonify(monans),200
    else:
        return jsonify({"message":"Not found!"}),404

@jwt_required()
def del_thuc_don(ma_td):
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    thuc_don = Thucdon.query.filter_by(ma_td=ma_td).first()
    if thuc_don :
        try:
            db.session.delete(thuc_don)
            db.session.commit()
        except Exception as e :
            db.session.rollback()
            return jsonify({"message":f"Error : {e}"}),409
        return jsonify({"message" : "Delete Access!"}),200
    else :
        return jsonify({"message":"Not found ma_td!"}),404
 
 
 # Quản lí món ăn

@jwt_required()
def add_mon_an():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if data:
        if ('ma_td' in data) and ('ten_mon' in data) and ('gia' in data) and ('hinhanh' in data):
            check_monan = Monan.query.filter_by(ten_mon=data['ten_mon']).first()
            if check_monan:
                return jsonify({"message":"ten_mon is exist!"}),409
            max_ma_mon = db.session.query(func.max(Monan.ma_mon)).scalar()
            ma_mon = int(max_ma_mon) + 1 if max_ma_mon is not None else 1
            ma_td = data['ma_td']
            ten_mon = data['ten_mon']
            gia = data['gia']
            soluong = 0
            hinhanh = data['hinhanh']
            try :
                monan = Monan(ma_mon=ma_mon,ma_td=ma_td,ten_mon=ten_mon,gia=gia,hinhanh=hinhanh,soluong=soluong)
                db.session.add(monan)
                db.session.commit()
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"}),409
            return jsonify({"message" : "Add successfuly!"}),201
        else:
            return jsonify({"message":"Request Error!"}),400
    else:
        return jsonify({"message":"Request Error!"}),400

@jwt_required()
def del_mon_an(ma_mon):
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    monan = Monan.query.filter_by(ma_mon=ma_mon).first()
    if monan:
        try:
            db.session.delete(monan)
            db.session.commit()
            return jsonify({"message":"Delete successfully!"}),200
        except Exception as e :
            db.session.rollback()
            return jsonify({"message":f"Error : {e}"}),409 
    else:
        return jsonify({"message":"Not found Mon An!"}),404
    
    

def get_all_mon_an():
    all_monan = Monan.query.all()
    if all_monan:
        return Monans_schema.jsonify(all_monan),200
    else:
        return jsonify({"message":"Not found Mon an!"}),404

@jwt_required()
def get_infor_monan_by_mamon(ma_mon):
    monan = Monan.query.filter_by(ma_mon=ma_mon).first()
    if monan:
        return Monan_schema.jsonify(monan),200
    else:
        return jsonify({"message":"Not found Mon an!"}),404

@jwt_required()
def update_gia_monan():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if data and ('ma_mon' in data) and ('gia' in data):
        ma_mon = data['ma_mon']
        gia = data['gia']
        monan = Monan.query.filter_by(ma_mon=ma_mon).first()
        if monan:
            try:
                monan.gia = gia
                db.session.commit()
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"}),409 
            return jsonify({"message":"Update successfully!"}),200
        else:
            return jsonify({"message":"Not found Mon an!"}),404
    else:
        return jsonify({"message":"Request Error!"}),400


@jwt_required()
def update_soluong_monan():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if data and ('ma_mon' in data) and ('soluong' in data):
        ma_mon = data['ma_mon']
        soluong = data['soluong']
        monan = Monan.query.filter_by(ma_mon=ma_mon).first()
        if monan:
            try:
                monan.soluong += soluong
                if monan.soluong < 0:
                    return jsonify({"message":"soluong is < 0"}),400
                db.session.commit()
            except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"}),409 
            return jsonify({"message":"Update successfully!"}),200
        else:
            return jsonify({"message":"Not found Mon an!"}),404
    else:
        return jsonify({"message":"Request Error!"}),400


# Quản lí voucher

@jwt_required()
def add_voucher():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if data and ('ma_voucher' in data) and ('phantram' in data) and ('dieukien' in data) and ('diem' in data) and ('soluong' in data):
        ma_voucher = data['ma_voucher']
        phantram = data['phantram']
        dieukien = data['dieukien']
        diem = data['diem']
        soluong = data['soluong']
        check_voucher = Voucher.query.filter_by(ma_voucher=ma_voucher).first()
        if check_voucher:
            return jsonify({"message":"Voucher is exist!"}),409
        voucher = Voucher(ma_voucher=ma_voucher,phantram=phantram,dieukien=dieukien,diem=diem,soluong=soluong)
        try:
            db.session.add(voucher)
            db.session.commit()
            return jsonify({"message":"Add Successfully!"}),201
        except Exception as e :
                db.session.rollback()
                return jsonify({"message":f"Error : {e}"}),409
    else:
        return jsonify({"message":"Request Error!"}),400

@jwt_required()
def del_voucher(ma_voucher):
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    voucher = Voucher.query.filter_by(ma_voucher=ma_voucher).first()
    if voucher:
        try:
            db.session.delete(voucher)
            db.session.commit()
            return jsonify({"message":"Delete successfully!"}),200
        except Exception as e :
            db.session.rollback()
            return jsonify({"message":f"Error : {e}"}),409  
    else:
       return jsonify({"message":"Not found Voucher!"}),404 

@jwt_required()
def update_voucher():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if not data or 'ma_voucher' not in data:
        return jsonify({"message": "Request Error!"}), 400

    voucher = Voucher.query.filter_by(ma_voucher=data['ma_voucher']).first()
    if not voucher:
        return jsonify({"message": "Not found voucher!"}), 404
    try:
        if 'phantram' in data:
            voucher.phantram = data['phantram']
        if 'dieukien' in data:
            voucher.dieukien = data['dieukien']
        if 'diem' in data:
            voucher.diem = data['diem']
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {e}"}), 409
    return jsonify({"message": "Update successfully"}), 200

        
@jwt_required()
def get_all_voucher():
    all_voucher = Voucher.query.all()
    if all_voucher:
        return Vouchers_schema.jsonify(all_voucher),200
    else:
       return jsonify({"message": "Not found voucher!"}), 404 

@jwt_required()
def get_infor_voucher(ma_voucher):
    voucher = Voucher.query.filter_by(ma_voucher=ma_voucher).first()
    if voucher :
        return Voucher_schema.jsonify(voucher),200
    else:
        return jsonify({"message": "Not found voucher!"}), 404 

@jwt_required()
def update_sl_voucher():
    if current_user.role != 'Quan Ly':
        return jsonify({"message":"Unauthorized"}),403
    data = request.json
    if data and ('ma_voucher' in data) and ('soluong' in data):
        voucher = Voucher.query.filter_by(ma_voucher=data['ma_voucher']).first()
        if voucher:
            try :
                voucher.soluong += data['soluong']
                db.session.commit()
                return jsonify({"message":"Update successfully"}),200
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": f"Error: {e}"}), 409
        else:
           return jsonify({"message": "Not found voucher!"}), 404  
    else:
        return jsonify({"message": "Request Error!"}), 400
    

