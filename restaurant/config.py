import os
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()
SECRET_KEY = os.environ.get('KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'thinh123'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

 