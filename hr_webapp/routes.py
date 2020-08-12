from flask import render_template, request, redirect, url_for
from hr_webapp import app
from hr_webapp.models import Checkin

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        latest_checkins = Checkin.query.order_by(Checkin.date).limit(10).all()
        return render_template('index.html', checkins=latest_checkins)
    # elif request.method == 'POST':
    # return """
    #     <h1>{{ row }}</h1>
    # """
