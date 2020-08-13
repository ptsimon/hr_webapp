from flask import render_template, request, redirect, url_for, jsonify
from hr_webapp import app
from hr_webapp.models import Checkin
from hr_webapp import db
from sqlalchemy import extract
from datetime import datetime

from io import TextIOWrapper
import csv
import os

from sqlalchemy.ext.declarative import DeclarativeMeta
import json

# json_file = os.getcwd()+'/hr_webapp/data.txt'
global json_data

@app.route('/data')
def returnData(*query):
    
    # with open(json_file) as jsonfile:
    #     return json.load(jsonfile)

    if query:
        list_dict = [x.as_dict() for x in query[0]]
        for_datatables = {'data': list_dict}
        global json_data
        json_data = jsonify(for_datatables)
    else:
        return json_data


@app.route('/', methods=['GET', 'POST'])
def index():
    # def datehandler(o):
    #     # if type(o) is datetime.date:
    #     #     return o.__str__()
    #     # # if isinstance(o, datetime):
    #     # #     return o.__str__()
    #     return o.__str__()

    # def writeToJSON(query):
    #     list_dict = [x.as_dict() for x in query]
    #     for_datatables = {'data': list_dict}

    #     with open(json_file, 'w') as outfile:
    #         json.dump(for_datatables, outfile, default=datehandler)

    if request.method == 'GET':
        latest_checkins = Checkin.query.order_by(Checkin.date.desc()).limit(100).all()
        returnData(latest_checkins)
        
        return render_template('index.html', checkins=latest_checkins, values={})
                    
    elif request.method == 'POST':
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
        
        returnData(query)
        
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