from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x13\xa5d>\xba\xd4g\xb3\x11\xdf\xbd\xd0\xbav\xe5m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkins.db'
db = SQLAlchemy(app)

db.create_all()

from hr_webapp import routes