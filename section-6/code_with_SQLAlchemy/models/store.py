from db import db
from models.item import ItemModel

class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic')
    
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod      # we are going to keep find_by_name as class_method since it returns object and not dictionary
    def find_by_name(cls, name):   # currently it returns ItemModel object, each row in SQLAlchemy db object is actually represent just that.
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    