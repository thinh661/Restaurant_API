from .extension import db
from sqlalchemy import func
from sqlalchemy import Column,Integer,Float,String,Date,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Sequence
class Users(db.Model) :
    user_name = Column(String(50),primary_key=True)
    email = Column(String(50))
    role = Column(String(50))
    password = Column(String(255))
    
    def __init__(self,user_name,email,password,role = 'Khach Hang'):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role =role
    

class Khachhang(db.Model):
    ma_kh = Column(Integer,primary_key=True)
    hoten = Column(String(255))
    ngaythamgia = Column(Date,default=func.now())
    doanhthu = Column(Float)
    diemtichluy = Column(Float)
    user_name = Column(String(150),ForeignKey('users.user_name'))
    
    def __init__(self,ma_kh,hoten,user_name,diemtichluy = 0,doanhthu = 0):
        self.hoten = hoten
        self.ma_kh = ma_kh
        self.doanhthu = doanhthu
        self.diemtichluy = diemtichluy
        self.user_name = user_name
    

class Nhanvien(db.Model):
    ma_nv = Column(Integer,primary_key=True,autoincrement=True)
    hoten = Column(String(255))
    ngayvaolam = Column(Date,default=func.now())
    chucvu = Column(String(50))
    user_name = Column(String(50),ForeignKey('users.user_name'))
    sdt = Column(String(50))
    
    def __init__(self,ma_nv,hoten,chucvu,user_name,sdt):
        self.hoten = hoten
        self.ma_nv = ma_nv
        self.chucvu = chucvu
        self.user_name = user_name
        self.sdt = sdt
        
class Ban(db.Model):
    ma_ban = Column(Integer,primary_key=True)
    ten_ban = Column(String(50))
    vitri = Column(String)
    soghe = Column(Integer)
    tinhtrang = Column(String(50))
    
    def __init__(self,ma_ban,ten_ban,vitri,soghe=0,tinhtrang='Con trong'):
        self.ten_ban = ten_ban
        self.ma_ban = ma_ban
        self.vitri = vitri
        self.soghe = soghe
        self.tinhtrang = tinhtrang
        
class Thucdon(db.Model):
    ma_td = Column(String(20),primary_key=True)
    ten_td = Column(String(50))
    mo_ta = Column(String(255))
    
    def __init__(self,ma_td,ten_td='Viet Nam',mo_ta = None):
        self.ma_td = ma_td
        self.ten_td = ten_td
        self.mo_ta = mo_ta
        
class Monan(db.Model):
    ma_mon = Column(Integer, primary_key=True)
    ma_td = Column(String(20), ForeignKey('thucdon.ma_td'))
    ten_mon = Column(String(255), nullable=False)
    gia = Column(Float, nullable=False)
    soluong = Column(Integer)
    thucdon = relationship('Thucdon', backref='monan')

    def __init__(self, ma_td, ten_mon, gia, soluong=None):
        self.ma_td = ma_td
        self.ten_mon = ten_mon
        self.gia = gia
        self.soluong = soluong

class Hoadon(db.Model):
    ma_hd = Column(Integer,primary_key=True)
    ma_kh = Column(Integer,ForeignKey('khachhang.ma_kh'))
    ma_ban = Column(Integer,ForeignKey('ban.ma_ban'))
    ngay = Column(DateTime,default=func.now())
    ma_voucher = Column(Integer,ForeignKey('voucher.ma_voucher'))
    tiengiam = Column(Float)
    tinhtrang = Column(String(50))
    loai = Column(String(50))
    
    def __init__(self,ma_hd,ma_kh,ma_ban,ma_voucher,tiengiam,tinhtrang="Chua thanh toan",loai="0"):
        self.ma_hd = ma_hd
        self.ma_ban= ma_ban
        self.ma_kh = ma_kh
        self.ma_voucher = ma_voucher
        self.tiengiam = tiengiam
        self.tinhtrang = tinhtrang
        
class Voucher(db.Model):
    ma_voucher = Column(Integer, primary_key=True)
    phantram = Column(Integer, nullable=False)
    dieukien = Column(String(50), nullable=False)
    diem = Column(Float)
    soluong = Column(Integer)

    def __init__(self, ma_voucher, phantram, dieukien, diem=None, soluong=None):
        self.ma_voucher = ma_voucher
        self.phantram = phantram
        self.dieukien = dieukien
        self.diem = diem
        self.soluong = soluong
    
class Cthd(db.Model):
    ma_hd = Column(Integer, ForeignKey('hoadon.ma_hd'), primary_key=True)
    ma_mon = Column(Integer, ForeignKey('monan.ma_mon'), primary_key=True)
    soluong = Column(Integer, nullable=False)
    thanhtien = Column(Float)

    def __init__(self, ma_hd, ma_mon, soluong, thanhtien):
        self.ma_hd = ma_hd
        self.ma_mon = ma_mon
        self.soluong = soluong
        self.thanhtien = thanhtien
        
class Phieuorder(db.Model):
    ma_phieu = Column(Integer,primary_key=True)
    ngayorder = Column(DateTime,default=func.now())
    thanhtien = Column(Float)
    
    def __init__(self,ma_phieu,ngayorder,thanhtien=0):
        self.ma_phieu = ma_phieu
        self.ngayorder = ngayorder
        self.thanhtien = thanhtien
    
class Nguyenlieu(db.Model):
    ma_nl = Column(Integer,primary_key=True)
    ten_nl = Column(String(50),nullable=False)
    dongia = Column(Float,nullable=False)
    donvi = Column(String)
    
    def __init__(self,ma_nl,ten_nl,dongia,donvi='g'):
        self.ma_nl = ma_nl
        self.ten_nl = ten_nl
        self.dongia = dongia
        self.donvi = donvi
    
class Ctorer(db.Model):
    ma_phieu = Column(Integer,ForeignKey('phieuorder.ma_phieu'),primary_key=True)
    ma_nl = Column(Integer,ForeignKey('nguyenlieu.ma_nl'),primary_key=True)
    soluong = Column(Integer)
    thanhtien = Column(Float)
    
    def __init__(self,ma_phieu,ma_nl,thanhtien,soluong=1) :
        self.ma_phieu = ma_phieu
        self.ma_nl = ma_nl
        self.thanhtien = thanhtien
        self.soluong = soluong
        

