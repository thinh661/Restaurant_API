from restaurant.extension import db
from restaurant.restaurant_ma import KhachhangChema,NhanvienSchema,UsersChema,BanSchema,HoadonSchema,MonanSchema,VoucherSchema,CthdSchema
from restaurant.models import Users,Nhanvien,Khachhang,Ban,Hoadon,Thucdon,Monan,Voucher,Cthd
from flask import request,jsonify
from sqlalchemy.sql import func
import json

Nhanvien_schema = NhanvienSchema()
Nhanviens_schema = NhanvienSchema(many=True)
Ban_schema = BanSchema()
Bans_schema = BanSchema(many=True)
Monan_schema = MonanSchema()
Monans_schema = MonanSchema(many=True)
Voucher_schema = VoucherSchema()
Vouchers_schema = VoucherSchema(many=True)
Hoadon_schema = HoadonSchema()
Hoadons_schema = HoadonSchema(many=True)
Cthds_schema = CthdSchema(many=True)
Cthd_schema = CthdSchema()

# Quản lí hóa đơn

def create_bill():
    data = request.json
    if data and ('ma_ban' in data) :
        ma_ban = data['ma_ban']
        max_ma_hd = db.session.query(func.max(Hoadon.ma_hd)).scalar()
        ma_hd = int(max_ma_hd) + 1 if max_ma_hd is not None else 1
        check_hoadon = Hoadon.query.filter_by(ma_ban=ma_ban,tinhtrang='Chua thanh toan').first()
        if check_hoadon:
            return jsonify({"message":"Invoice cannot be created because this table has not yet paid!"}),409
        try :
            hoadon = Hoadon(ma_hd=ma_hd,ma_ban=ma_ban)
            db.session.add(hoadon)
            db.session.commit()
            return jsonify({"message":"Bill Created!"}),201
        except Exception as e :
            db.session.rollback()
            return jsonify({"message":f"Error : {e}"}),409
    else:
        return jsonify({"message": "Request Error!"}), 400

def get_bill_by_ma_hd(ma_hd):
    hoadon = Hoadon.query.filter_by(ma_hd=ma_hd).first()
    if hoadon:
        return Hoadon_schema.jsonify(hoadon),200
    else :
        return jsonify({"message": "Not found bill"}),400

def get_all_bill_unpaid():
    hoadons = Hoadon.query.filter_by(tinhtrang='Chua thanh toan').all()
    if hoadons:
        return Hoadons_schema.jsonify(hoadons),200
    else:
        return jsonify({"message": "Not found bill"}),400

def add_ma_kh_into_bill():
    data = request.json
    if data and ('ma_hd' in data) and ('ma_kh' in data):
        khachhang = Khachhang.query.filter_by(ma_kh=data['ma_kh']).first()
        if khachhang:
            diemtichluy = khachhang.diemtichluy
            hoadon = Hoadon.query.filter_by(ma_hd=data['ma_hd']).first()
            if hoadon:
                try:
                    if hoadon.ma_voucher is not None:
                        voucher = Voucher.query.filter_by(ma_voucher=hoadon.ma_voucher).first()
                        if voucher.soluong > 0 and diemtichluy >= voucher.diem :
                            hoadon.tiengiam = (hoadon.tienmonan*voucher.phantram)/100
                    hoadon.ma_kh = data['ma_kh']
                    db.session.commit()
                    return jsonify({"message":"Add successfully!"}),200
                except Exception:
                    db.session.rollback()
                    return jsonify({"message":"Can't add ma_kh!"}),409
            else:
                return jsonify({"message": "Not found bill!"}),400   
        else:
            return jsonify({"message": "Not found customer!"}),400

def add_tienmonan_into_bill(ma_hd):
    hoadon = Hoadon.query.filter_by(ma_hd=ma_hd).first()
    if hoadon:
        try:
            lst = get_detail_bill_by_ma_hd(ma_hd=ma_hd)
            res = 0
            for i in lst:
                res += i['thanhtien']
            hoadon.tienmonan = res
            db.session.commit()
            return jsonify({"message":"Add Success!"}),200
        except Exception:
            db.session.rollback()
            return jsonify({"message":"Can't add ma_kh!"}),409
    else:
        return jsonify({"message":"Not found detail bill!"}),400
    

def add_voucher():
    data = request.json
    if data and ('ma_hd' in data) and ('ma_voucher' in data):
        hoadon = Hoadon.query.filter_by(ma_hd=data['ma_hd']).first()
        if hoadon and (hoadon.ma_voucher is None):
            voucher = Voucher.query.filter_by(ma_voucher=data['ma_voucher']).first()
            if voucher and (voucher.soluong <= 0):
                try:
                    hoadon.ma_voucher = data['ma_voucher']
                    if hoadon.ma_kh is not None:
                        khachhang = Khachhang.query.filter_by(ma_kh=hoadon.ma_kh).first()
                        diemtichluy = khachhang.diemtichluy
                        if diemtichluy >= voucher.diem :
                            hoadon.tiengiam = (hoadon.tienmonan*voucher.phantram)/100
                    db.session.commit()
                    return jsonify({"message":"Add successfully!"}),200
                except Exception:
                    db.session.rollback()
                    return jsonify({"message":"Can't add voucher!"}),409
            else :
                return jsonify({"message": "Not found voucher!"}),400
        else:
            return jsonify({"message": "Not found bill or bill had voucher!"}),400     
    else:
        return jsonify({"message": "Request Error!"}),400

def thanh_toan_bill(ma_hd):
    hoadon = Hoadon.query.filter_by(ma_hd=ma_hd).first()
    if hoadon:
        try:
            if (hoadon.ma_kh is not None) and (hoadon.ma_voucher is not None):
                khachhang = Khachhang.query.filter_by(ma_kh=hoadon.ma_kh).first()
                voucher = Voucher.query.filter_by(ma_voucher=hoadon.ma_voucher).first()
                khachhang.diemtichluy -= voucher.diem
                voucher.soluong -= 1
            if (hoadon.ma_kh is not None) and (hoadon.ma_voucher is None):
                khachhang = Khachhang.query.filter_by(ma_kh=hoadon.ma_kh).first()
                khachhang.diemtichluy += 100
            hoadon.tinhtrang = 'Da thanh toan'
            tongtien = hoadon.tienmonan - hoadon.tiengiam
            db.session.commit()
            return jsonify({"message":"Payment success!"},{"tong_tien":f"{tongtien}"}),200
        except Exception:
                db.session.rollback()
                return jsonify({"message":"Can't payment bill!"}),409
    else:
        return jsonify({"message": "Not found bill!"}),400  

# Quản lí chi tiết hóa đơn

def add_monan_into_cthd():
    data = request.json
    if data and ('ma_hd' in data) and ('ma_mon' in data) and ('soluong' in data) :
        ma_hd = data['ma_hd']
        ma_mon = data['ma_mon']
        soluong = data['soluong']
        monan = Monan.query.filter_by(ma_mon=ma_mon).first()
        hoadon = Hoadon.query.filter_by(ma_hd=ma_hd).first()
        if not monan or not hoadon:
            return jsonify({"message":"Not found ma_mon or ma_hd"}),409
        thanhtien = monan.gia*soluong
        try:
            check_cthd = Cthd.query.filter_by(ma_hd=ma_hd,ma_mon=ma_mon).first()
            if check_cthd:
                check_cthd.soluong += soluong
                check_cthd.thanhtien += thanhtien
                db.session.commit()
                return jsonify({"message":"Add success!"}),201
            else:
                cthd = Cthd(ma_hd=ma_hd,ma_mon=ma_mon,soluong=soluong,thanhtien=thanhtien)
                db.session.add(cthd)
                db.session.commit()
                return jsonify({"message":"Add success!"}),201
        except Exception:
            db.session.rollback()
            return jsonify({"message":"Can't add voucher!"}),409
    else:
        return jsonify({"message": "Request Error!"}),400

def get_detail_bill_by_ma_hd(ma_hd):
    cthds = Cthd.query.filter_by(ma_hd=ma_hd).all()
    if cthds:
        return Cthds_schema.jsonify(cthds),200
    else:
        return jsonify({"message":"Detail bill is empty!"}),400