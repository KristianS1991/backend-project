from db import db


class TweetModel(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    data = db.Column(db.String(600))

    category_item_id = db.Column(db.Integer, db.ForeignKey('category_items.id'))
    category_item = db.relationship('CategoryItemModel')

    def __init__(self, category_item_id, username, data):
        self.category_item_id = category_item_id
        self.username = username
        self.data = data

    def json(self):
        return {
            'id': self.id, 
            'username': self.username,
            'category_item_id': self.category_item_id,
            'data': self.data
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
