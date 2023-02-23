from . import db


class UserInfo(db.Model):
    """
    用户表
    """
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __str__(self):
        return '<User %r>' % self.username

    def __repr__(self):
        return '<User %r>' % self.username
