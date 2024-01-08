from .extension import ma

class UsersChema(ma.Schema):
    class Meta():
        fields = ('user_name','email','role','password')
        
class KhachhangChema(ma.Schema):
    class Meta():
        fields = ('ma_kh','hoten','ngaythamgia','doanhthu','diemtichluy','user_name')

class NhanvienSchema(ma.Schema):
    class Meta():
        fields = ('ma_nv','hoten','ngayvaolam','chucvu','user_name','sdt')
        
class BanSchema(ma.Schema):
    class Meta():
        fields = ('ma_ban','ten_ban','vitri','soghe','tinhtrang')

class HoadonSchema(ma.Schema):
    class Meta():
        fields = ('ma_hd','ma_kh','ma_ban','ngay','tienmonan','ma_voucher','tiengiam','tinh trang','loai')
        
class CthdSchema(ma.Schema):
    class Meta():
        fields = ('ma_hd','ma_mon','soluong','thanhtien')
        
class ThucdonSchema(ma.Schema):
    class Meta():
        fields = ('ma_td','ten_td','mo_ta')

class MonanSchema(ma.Schema):
    class Meta():
        fields = ('ma_mon','ma_td','ten_mon','gia','soluong','hinhanh')
        
class VoucherSchema(ma.Schema):
    class Meta():
        fields = ('ma_voucher','phantram','dieukien','diem','soluong')
        
class NguyenlieuSchema(ma.Schema):
    class Meta():
        fields = ('ma_nl','ten_nl','dongia','donvi')
    
class PhieuorderSchema(ma.Schema):
    class Meta():
        fields = ('ma_phieu','ngayorder','thanhtien')

class CtorderSchema(ma.Schema):
    class Meta():
        fields = ('ma_phieu','ma_nl','soluong','thanhtien')

class OrdercthdSchema(ma.Schema):
    class Meta():
        fields = ('ma_order','ma_hd','ten_mon','soluong','ten_ban','tinhtrang')

