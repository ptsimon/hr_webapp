from flask import render_template, request, redirect, url_for, jsonify
from hr_webapp import app
from hr_webapp.models import Checkin

from io import TextIOWrapper
import csv

# from sqlalchemy.ext.declarative import DeclarativeMeta
# import json
# class AlchemyEncoder(json.JSONEncoder):

#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields

#         return json.JSONEncoder.default(self, obj)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        latest_checkins = Checkin.query.order_by(Checkin.date).limit(50).all()
        # json_checkins = json.dumps(latest_checkins, cls=AlchemyEncoder)
        return render_template('index.html', 
                    checkins=latest_checkins, values={}, 
                    # json_checkins=json_checkins
                    )
    elif request.method == 'POST':
        user_id = request.form['user_id']
        query = Checkin.query.filter_by(user_id=user_id).order_by(Checkin.date).all()
        values = {
            "user_id": user_id
        }
        return render_template('index.html', checkins=query, values=values)

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