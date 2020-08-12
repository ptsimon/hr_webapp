from datetime import datetime
from hr_webapp import db

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    project_id = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<CheckIn %r>' % (str(self.date), str(self.user_id), str(self.hours))