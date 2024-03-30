from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(50))  # Tutor or Tutee

    # Polymorphic identity configuration
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Tutor(User):
    __mapper_args__ = {'polymorphic_identity': 'tutor'}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    available_times = db.relationship('Time', backref='tutor', lazy=True)


class Tutee(User):
    __mapper_args__ = {'polymorphic_identity': 'tutee'}
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


# Each Time instance is a 30-minute time-slot, making it sufficient to just have start_time
class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=True)


# A Class instance is created only when tutee registers a class
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=True)
    tutee_id = db.Column(db.Integer, db.ForeignKey('tutee.id'), nullable=True)
