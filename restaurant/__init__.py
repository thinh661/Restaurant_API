from flask import Flask,Blueprint,request,jsonify
from .extension import db,ma,jwt
from .models import Users,Nhanvien,Khachhang
from .users.controller import users
from .quanli.controller import quanli
from .khachhang.controller import khachhang
from .hoadon.controller import hoadon
from .daubep.controller import daubep


def create_db(app):
    db.create_all(app)
    print('Da tao DB!')
    
def create_app(config_file = "config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app=app)
    ma.init_app(app=app)
    jwt.init_app(app=app)
    
    app.register_blueprint(users)
    app.register_blueprint(quanli)
    app.register_blueprint(khachhang)
    app.register_blueprint(hoadon)
    app.register_blueprint(daubep)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers,jwt_data):
        identity = jwt_data['sub']
        return Users.query.filter_by(user_name=identity).one_or_none()
    
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({'error':"token_expired"}),401
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error":"invalid_token"}),401
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"error":"unauthorized_header"}),401
    
    return app