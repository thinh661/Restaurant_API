from flask import Blueprint
from .service import add_nguyenlieu,del_nguyenlieu,create_phieuorder,add_thanhtien_into_phieuorder,get_phieuorder,add_nguyenlieu_into_ctorder,get_ctorder,get_all_nguyenlieu


daubep = Blueprint("daubep",__name__)

# Quản lí nguyên liệu

@daubep.route('/api/nguyenlieu/add',methods=['POST'])
def add_nl():
    return add_nguyenlieu()

@daubep.route('/api/nguyenlieu/del/<int:ma_nl>',methods=['DELETE'])
def del_nl(ma_nl):
    return del_nguyenlieu(ma_nl=ma_nl)

@daubep.route('/api/nguyenlieu/all',methods=['GET'])
def all_nl():
    return get_all_nguyenlieu()

# Quản lí phiếu order 

@daubep.route('/api/phieuorder/add',methods=['POST'])
def create_order():
    return create_phieuorder()

@daubep.route('/api/phieuorder/update-thanhtien/<int:ma_phieu>',methods=['PUT'])
def update_thanhtien(ma_phieu):
    return add_thanhtien_into_phieuorder(ma_phieu=ma_phieu)

@daubep.route('/api/phieuorder/infor/<int:ma_phieu>',methods=['GET'])
def get_infor_phieuorder(ma_phieu):
    return get_phieuorder(ma_phieu=ma_phieu)

# Quản lí chi tiết order 

@daubep.route('/api/ctorder/add',methods=['POST'])
def create_ctorder():
    return add_nguyenlieu_into_ctorder()

@daubep.route('/api/ctorder/infor/<int:ma_phieu>',methods=['GET'])
def get_infor_by_maphieu(ma_phieu):
    return get_ctorder(ma_phieu=ma_phieu)



