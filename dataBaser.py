from init import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    pw_hash = db.Column(db.String(64))

    budgetData = db.relationship('Budget', backref='user')
    budgetTotal = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.name


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    value = db.Column(db.Float)

    # 0 is Income, 1 is Expense
    type = db.Column(db.Boolean)

    def __repr__(self):
        return '<Budget '+self.name+', '+str(self.value)+'>'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(200))
    ctime = db.Column(db.String(40))
    time = db.Column(db.Integer)
    replies = db.relationship('Reply', backref='post')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # creator_id holds the ID of a valid user


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    pid = db.Column(db.Integer, db.ForeignKey('post.id'))
    body = db.Column(db.String(200))


db.create_all(app=app)

