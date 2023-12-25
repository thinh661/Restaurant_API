from flask import Blueprint
from .service import add_staff,delete_staff,get_all_staff,get_staff_by_name,fix_staff,add_table,delete_table,book_seat,cancel_book_seat,get_all_table,get_table_by_name

quanli = Blueprint("quanli",__name__)

@quanli.route('/api/infor-staff',methods=['GET'])
def infor_all_staff():
    return get_all_staff()

@quanli.route('/api/infor-staff/<string:name>',methods=['GET'])
def infor_staff_by_name(name):
    return get_staff_by_name(name=name)

@quanli.route('/api/infor-staff/add-staff',methods=['POST'])
def add_infor_staff():
    return add_staff()

@quanli.route('/api/infor-staff/delete-staff/<int:ma_nv>',methods=['DELETE'])
def delete_infor_staff(ma_nv):
    return delete_staff(ma_nv=ma_nv)

@quanli.route('/api/infor-staff/fix-infor-staff/<int:ma_nv>',methods=['PUT'])
def fix_infor_staff(ma_nv):
    return fix_staff(ma_nv=ma_nv)

@quanli.route('/api/table/add-table',methods=['POST'])
def ql_add_table():
    return add_table()

@quanli.route('/api/table/delete-table/<int:ma_ban>',methods=['DELETE'])
def delete_table_by_ma_ban(ma_ban):
    return delete_table(ma_ban=ma_ban)

@quanli.route('/api/table/infor-table/all',methods=['GET'])
def infor_all_table():
    return get_all_table()

@quanli.route('/api/table/infor-table/<string:ten_ban>',methods=['GET'])
def infor_table_by_name(ten_ban):
    return get_table_by_name(ten_ban=ten_ban)

@quanli.route('/api/table/book-table/<string:ten_ban>',methods=['PUT'])
def book_table(ten_ban):
    return book_seat(ten_ban=ten_ban)

@quanli.route('/api/table/cancel-booking/<string:ten_ban>',methods=['PUT'])
def cancel_booking(ten_ban):
    return cancel_book_seat(ten_ban=ten_ban)