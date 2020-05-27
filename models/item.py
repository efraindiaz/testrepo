#import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, id, name, price, store_id):
        self.id = id
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'id':self.id,'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        #first row only
        return ItemModel.query.filter_by(name=name).first() #select * from items where name=name limit 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name=?"
        cursor.execute(query, (self.price,self.name))
        connection.commit()
        connection.close()