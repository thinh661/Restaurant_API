from restaurant.extension import db
from restaurant.restaurant_ma import KhachhangChema,NhanvienSchema,UsersChema,BanSchema,HoadonSchema,MonanSchema,VoucherSchema,CthdSchema,CtorderSchema,NguyenlieuSchema,PhieuorderSchema
from restaurant.models import Users,Nhanvien,Khachhang,Ban,Hoadon,Thucdon,Monan,Voucher,Cthd,Nguyenlieu,Phieuorder,Ctorder
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
Nguyenlieus_schema = NguyenlieuSchema(many=True)
Phieuorder_schema = PhieuorderSchema()
Ctorders_schema = CtorderSchema(many=True)

# Quản lí nguyên liệu

def add_nguyenlieu():
    data = request.json
    if data and ('ten_nl' in data) and ('dongia' in data) and ('donvi' in data):
        check_nguyenlieu = Nguyenlieu.query.filter_by(ten_nl=data['ten_nl']).first()
        if check_nguyenlieu :
            return jsonify({"message":"ten_nl is exist!"}),409
        try:
            max_ma_nl = db.session.query(func.max(Nguyenlieu.ma_nl)).scalar()
            ma_nl = int(max_ma_nl) + 1 if max_ma_nl is not None else 1
            nguyenlieu = Nguyenlieu(ma_nl=ma_nl,ten_nl=data['ten_nl'],dongia=data['dongia'],donvi=data['donvi'])
            db.session.add(nguyenlieu)
            db.session.commit()
            return jsonify({"message":"Add success!"}),200
        except Exception:
            db.session.rollback()
            return jsonify({"message":"Can Add!"}),409
    else:
        return jsonify({"message":"Request Error!"}),400

def del_nguyenlieu(ma_nl):
    nguyenlieu = Nguyenlieu.query.filter_by(ma_nl=ma_nl).first()
    if nguyenlieu:
        try:
            db.session.delete(nguyenlieu)
            db.session.commit()
            return jsonify({"message":"Delete access!"}),200
        except Exception:
            db.session.rollback()
            return jsonify({"message":"Can delete!"}),409
    else:
        return jsonify({"message":"Not found!"}),400

def get_all_nguyenlieu():
    all_nl = Nguyenlieu.query.all()
    if all_nl:
        return Nguyenlieus_schema.jsonify(all_nl),200
    else:
        return jsonify({"message":"Not found!"}),400

# Quản lí phiếu order 

def create_phieuorder():
    try:
        max_ma_phieu = db.session.query(func.max(Phieuorder.ma_phieu)).scalar()
        ma_phieu = int(max_ma_phieu) + 1 if max_ma_phieu is not None else 1
        phieuorder = Phieuorder(ma_phieu=ma_phieu,thanhtien=0)
        db.session.add(phieuorder)
        db.session.commit()
        return jsonify({"message":"Create success!"},{"ma_phieu" : f"{ma_phieu}"}),200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"Can't create!"}),409

def add_thanhtien_into_phieuorder(ma_phieu):
    phieuorder = Phieuorder.query.filter_by(ma_phieu=ma_phieu).first()
    if not phieuorder:
        return jsonify({"message":"Not found!"}),400
    try:
        total_thanhtien = db.session.query(func.sum(Ctorder.thanhtien)).filter_by(ma_phieu=ma_phieu).scalar()
        total_thanhtien = total_thanhtien if total_thanhtien is not None else 0
        phieuorder.thanhtien = total_thanhtien
        db.session.commit()
        return jsonify({"message":"Add success!"}),200
    except Exception:
        db.session.rollback()
        return jsonify({"message":"Can add!"}),409

def get_phieuorder(ma_phieu):
    phieuorder = Phieuorder.query.filter_by(ma_phieu=ma_phieu).first()
    if phieuorder:
        return Phieuorder_schema.jsonify(phieuorder),200
    else:
        return jsonify({"message":"Not found!"}),400

# Quản lí chi tiết order 

def add_nguyenlieu_into_ctorder():
    data = request.json
    if data and ('ma_phieu' in data) and ('ma_nl' in data) and ('soluong' in data):
        phieuorder = Phieuorder.query.filter_by(ma_phieu=data['ma_phieu']).first()
        nguyenlieu = Nguyenlieu.query.filter_by(ma_nl=data['ma_nl']).first()
        if not phieuorder or not nguyenlieu:
            return jsonify({"message":"Not add ma_phieu or ma_nl"}),409
        thanhtien = nguyenlieu.dongia*data['soluong']
        try:
            check_ctorder = Ctorder.query.filter_by(ma_phieu=data['ma_phieu'],ma_nl=data['ma_nl']).first()
            if check_ctorder:
                check_ctorder.soluong += data['soluong']
                check_ctorder.thanhtien += thanhtien
                db.session.commit()
                return jsonify({"message":"Add success!"}),201
            else:
                ctorder = Ctorder(ma_phieu=data['ma_phieu'],ma_nl=data['ma_nl'],soluong=data['soluong'],thanhtien=thanhtien)
                db.session.add(ctorder)
                db.session.commit()
                return jsonify({"message":"Add success!"}),201
        except Exception:
            db.session.rollback()
            return jsonify({"message":"Can add!"}),409
    else:
        return jsonify({"message":"Request Error!"}),400

def get_ctorder(ma_phieu):
    all_crorder = Ctorder.query.filter_by(ma_phieu=ma_phieu).all()
    if all_crorder:
        return Ctorders_schema.jsonify(all_crorder),200
    else:
       return jsonify({"message":"Not found!"}),400 
