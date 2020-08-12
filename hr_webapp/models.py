from datetime import datetime
from hr_webapp import db

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    project_id = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"CheckIn('{strself.date}', '{self.user_id}', '{self.hours}')"