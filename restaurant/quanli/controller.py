from flask import Blueprint
from .service import (
    add_staff, delete_staff, get_all_staff, get_staff_by_name,
    fix_staff, add_table, delete_table, book_seat, cancel_book_seat,
    get_all_table, get_table_by_name, add_thuc_don, del_thuc_don,
    add_mon_an, del_mon_an, get_all_mon_an, get_infor_monan_by_mamon,
    get_infor_voucher, get_all_voucher,update_gia_monan,update_soluong_monan,
    add_voucher,del_voucher,update_voucher,update_sl_voucher,finish_table,start_table,get_all_thucdon,
    get_all_monan_by_ma_td,get_ten_thucdon_by_ma_td
)
from flask_jwt_extended import jwt_required


quanli = Blueprint("quanli",__name__)

# Quản lí nhân viên

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

# Quản lí bàn 

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

@quanli.route('/api/table/finish/<string:ten_ban>',methods=['PUT'])
def finish_tab(ten_ban):
    return finish_table(ten_ban=ten_ban)

@quanli.route('/api/table/start/<string:ten_ban>',methods=['PUT'])
def start_tab(ten_ban):
    return start_table(ten_ban=ten_ban)

# Quản lí thực đơn

@quanli.route('/api/thucdon/add-thuc-don',methods=['POST'])
def add_td():
    return add_thuc_don()

@quanli.route('/api/thucdon/del-thuc-don/<int:ma_td>',methods=['DELETE'])
def del_td(ma_td):
    return del_thuc_don(ma_td=ma_td)

@quanli.route('/api/thucdon/all',methods=['GET'])
def all_thucdon():
    return get_all_thucdon()

@quanli.route('/api/thucdon-monan/<int:ma_td>',methods=['GET'])
def get_all_monan_by_matd(ma_td):
    return get_all_monan_by_ma_td(ma_td=ma_td)
        
@quanli.route('/api/thucdon/ten_td/<int:ma_td>',methods=['GET'])
def get_tentd_by_ma_td(ma_td):
    return get_ten_thucdon_by_ma_td(ma_td=ma_td)

# Quản lí món ăn

@quanli.route('/api/monan/add-mon-an',methods=['POST'])
def add_monan():
    return add_mon_an()

@quanli.route('/api/monan/del-mon-an/<int:ma_mon>',methods=['DELETE'])
def del_monan(ma_mon):
    return del_mon_an(ma_mon=ma_mon)

@quanli.route('/api/monan/all',methods=['GET'])
def get_all_monan():
    return get_all_mon_an()

@quanli.route('/api/monan/<int:ma_mon>',methods=['GET'])
def get_infor_by_mamon(ma_mon):
    return get_infor_monan_by_mamon(ma_mon=ma_mon)

@quanli.route('/api/monan/update-gia',methods=['PUT'])
def update_gia():
    return update_gia_monan()

@quanli.route('/api/monan/update-soluong',methods=['PUT'])
def update_soluong():
    return update_soluong_monan()

# Quản lí voucher

@quanli.route('/api/voucher/add-voucher',methods=['POST'])
def add_vou():
    return add_voucher()

@quanli.route('/api/voucher/del-voucher/<int:ma_voucher>',methods=['DELETE'])
def del_vou(ma_voucher):
    return del_voucher(ma_voucher=ma_voucher)

@quanli.route('/api/voucher/update-voucher',methods=['PUT'])
def update_vou():
    return update_voucher()

@quanli.route('/api/voucher/all',methods=['GET'])
def get_all_vou():
    return get_all_voucher()

@quanli.route('/api/voucher/<int:ma_voucher>',methods=['GET'])
def infor_voucher(ma_voucher):
    return get_infor_voucher(ma_voucher=ma_voucher)

@quanli.route('/api/voucher/update-sl-voucher',methods=['PUT'])
def update_sl_vou():
    return update_sl_voucher()