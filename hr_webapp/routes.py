from flask import render_template, request, redirect, url_for
from hr_webapp import app
from hr_webapp.models import Checkin

from io import TextIOWrapper
import csv

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        latest_checkins = Checkin.query.order_by(Checkin.date).limit(100).all()
        return render_template('index.html', checkins=latest_checkins)
    elif request.method == 'POST':
        user_id = request.form['user_id']
        query = Checkin.query.filter_by(user_id=user_id).order_by(Checkin.date).all()
        return render_template('index.html', checkins=query)

@app.route('/uploadcsv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] != "date":
                
                checkin = EmployeeCheckin(
                            date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                            project_id=row[1],
                            manager_id=row[2],
                            user_id=row[3],
                            hours=row[4])
                db.session.add(checkin)
                db.session.commit()
        # return redirect('/uploadcsv')
        return redirect(url_for('upload_csv'))
    return """
            <form method='post' action='/' enctype='multipart/form-data'>
              Upload a csv file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
           """  