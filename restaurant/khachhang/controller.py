from flask import Blueprint
from .service import update_hoten,get_info_khach_hang
from .service import book_seat,cancel_book_seat

khachhang = Blueprint("khachhang",__name__)

@khachhang.route('/api/khach-hang/infor/<string:user_name>',methods=['GET'])
def info_khach_hang(user_name):
    return get_info_khach_hang(user_name=user_name)

@khachhang.route('/api/khach-hang/update-info/<string:user_name>',methods=['PUT'])
def update_hoten_kh(user_name):
    return update_hoten(user_name=user_name)

@khachhang.route('/api/khach-hang/book-seat/<string:ten_ban>',methods=['POST'])
def booking_seat(ten_ban):
    return book_seat(ten_ban=ten_ban)

@khachhang.route('/api/khach-hang/cancel-book-seat/<string:ten_ban>',methods=['PUT'])
def cancel_booking_seat(ten_ban):
    return cancel_book_seat(ten_ban=ten_ban)