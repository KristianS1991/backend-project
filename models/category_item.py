from db import db


class CategoryItemModel(db.Model):
    __tablename__ = 'category_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel')

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def json(self):
        return {
            'id': self.id, 
            'name': self.name,
            'category_id': self.category_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
