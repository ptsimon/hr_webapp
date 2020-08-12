from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import TextIOWrapper
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x13\xa5d>\xba\xd4g\xb3\x11\xdf\xbd\xd0\xbav\xe5m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkins.db'

db = SQLAlchemy(app)

class EmployeeCheckin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    project_id = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<CheckIn %r>' % (str(self.date), str(self.user_id), str(self.hours))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        latest_checkins = EmployeeCheckin.query.order_by(EmployeeCheckin.date).limit(10).all()
        return render_template('index.html', checkins=latest_checkins)
    # elif request.method == 'POST':
    # return """
    #     <h1>{{ row }}</h1>
    # """
    

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)