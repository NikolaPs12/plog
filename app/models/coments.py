from ..extensions import db
from flask_login import UserMixin
from datetime import datetime
class Coment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    author = db.relationship('User', backref=db.backref('coments', lazy=True))
    post = db.relationship('Post', backref=db.backref('coments', lazy=True))

    def __repr__(self):
        return f'<Coment {self.content[:20]}>'