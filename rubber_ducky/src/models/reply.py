
import datetime

from .. import db


class Reply(db.Model):

    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.public_id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime)
