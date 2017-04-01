from init import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    pw_hash = db.Column(db.String(64))

    budgetData = db.relationship('Budget', backref='user')
    budgetTotal = db.Column(db.Float)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    value = db.Column(db.Float)

    # 0 is Income, 1 is Expense
    type = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


db.create_all(app=app)

