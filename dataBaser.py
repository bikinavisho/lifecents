from LifeCents import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    pw_hash = db.Column(db.String(64))

    budgetData = db.relationship('Budget', backref='user')


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    value = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


db.create_all(app=app)

