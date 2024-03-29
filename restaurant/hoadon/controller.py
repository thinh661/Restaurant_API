from flask import Blueprint
from .service import create_bill,get_bill_by_ma_hd,add_ma_kh_into_bill,add_tienmonan_into_bill,add_voucher,thanh_toan_bill,add_monan_into_cthd,get_detail_bill_by_ma_hd,get_all_bill_unpaid,get_all_ordercthd_unpaid,finish_ordercthd,get_all_bill_by_day,get_revenue_on_week


hoadon = Blueprint("hoadon",__name__)

# Quản lí hóa đơn

@hoadon.route('/api/hoadon/create-bill',methods=['POST'])
def created_bill():
    return create_bill()

@hoadon.route('/api/hoadon/get-bill/<int:ma_hd>',methods=['GET'])
def get_bill_by_mahd(ma_hd):
    return get_bill_by_ma_hd(ma_hd=ma_hd)

@hoadon.route('/api/hoadon/get-bill/all',methods=['GET'])
def all_bill_unpaid():
    return get_all_bill_unpaid()

@hoadon.route('/api/hoadon/update-makh-bill',methods=['PUT'])
def add_makh_into_bill():
    return add_ma_kh_into_bill()

@hoadon.route('/api/hoadon/update-tienmonan-bill/<int:ma_hd>',methods=['PUT'])
def update_tienmonan_bill(ma_hd):
    return add_tienmonan_into_bill(ma_hd=ma_hd)

@hoadon.route('/api/hoadon/update-voucher-bill',methods=['PUT'])
def update_voucher_bill():
    return add_voucher()

@hoadon.route('/api/hoadon/update-pay-bill/<int:ma_hd>',methods=['PUT'])
def pay_bill(ma_hd):
    return thanh_toan_bill(ma_hd=ma_hd)

@hoadon.route('/api/hoadon/get-bill/allday',methods=['GET'])
def all_bill_by_day():
    return get_all_bill_by_day()

@hoadon.route('/api/hoadon/revenue/week',methods=['GET'])
def revenue_on_week():
    return get_revenue_on_week()

# Quản lí chi tiết hóa đơn

@hoadon.route('/api/cthd/add',methods=['POST'])
def add_monan_cthd():
    return add_monan_into_cthd()

@hoadon.route('/api/cthd/<int:ma_hd>',methods=['GET'])
def get_detail_bill_by_mahd(ma_hd):
    return get_detail_bill_by_ma_hd(ma_hd=ma_hd)

@hoadon.route('/api/ordercthd/all-unpaid',methods=['GET'])
def all_ordercthd_unpaid():
    return get_all_ordercthd_unpaid()

@hoadon.route('/api/ordercthd/finish-ordercthd/<int:ma_order>',methods=['PUT'])
def finish_ordercthd_unpaid(ma_order):
    return finish_ordercthd(ma_order=ma_order)
    
