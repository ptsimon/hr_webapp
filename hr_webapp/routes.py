from flask import render_template, request, redirect, url_for, jsonify
from hr_webapp import app
from hr_webapp.models import Checkin
from hr_webapp import db
from sqlalchemy import extract
from datetime import datetime

from io import TextIOWrapper
import csv

from sqlalchemy.ext.declarative import DeclarativeMeta
import json
class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

@app.route('/data')
def data():
    latest_checkins = Checkin.query.order_by(Checkin.date.desc()).limit(50).all()
    list_dict = [x.as_dict() for x in latest_checkins]
    for_datatables = {'data': list_dict}
    print("aaa", for_datatables['data'][0]['date'])
    return (jsonify(for_datatables))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        latest_checkins = Checkin.query.order_by(Checkin.date.desc()).limit(50).all()
        print 
        # return (jsonify(json_checkins))
        return render_template('index.html', 
                    checkins=latest_checkins, values={}, 
                    # json_checkins=json_checkins
                    )
    elif request.method == 'POST':
        print (request.form)
        query = Checkin.query
        filters = {k: v for k, v in request.form.items() if v != '' and k != 'month'}
        
        #if empty form values
        if not filters and request.form['month']=='':
            return redirect(url_for('index'))
        
        if request.form['user_id'] or request.form['project_id']:
            query = query.filter_by(**filters).order_by(Checkin.date)

        if request.form['month']:
            year, month = [int(x.lstrip('0')) for x in request.form['month'].split('-')]
            query = query.filter(extract('year', Checkin.date)==year).filter(extract('month', Checkin.date)==month).order_by(Checkin.date)
        
        return render_template('index.html', checkins=query, values=request.form)

@app.route('/uploadcsv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] != "date":
                
                checkin = Checkin(
                            date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                            project_id=row[1],
                            manager_id=row[2],
                            user_id=row[3],
                            hours=row[4])
                db.session.add(checkin)
                db.session.commit()
                
        return redirect(url_for('upload_csv'))

    return """
            <form method='post' action='/uploadcsv' enctype='multipart/form-data'>
              Upload a csv file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
            <a href="/">Go Back</a>
           """  