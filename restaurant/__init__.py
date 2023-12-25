from flask import Flask,Blueprint,request
from .extension import db,ma
from .models import Users,Nhanvien,Khachhang
from .users.controller import users
from .quanli.controller import quanli
from .khachhang.controller import khachhang


def create_db(app):
    db.create_all(app)
    print('Da tao DB!')
    
def create_app(config_file = "config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app=app)
    ma.init_app(app=app)
    
    app.register_blueprint(users)
    app.register_blueprint(quanli)
    app.register_blueprint(khachhang)
    return app