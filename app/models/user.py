from typing import AnyStr
from app.providers.database import db


class User(db.Model):
    
    public_key: AnyStr
    private_key: AnyStr

    __table__ = 'users'

    __fillable__ = ['username']
    __primary_key__ = 'id'
    __guarded__ = ['id', 'public_key', 'private_key']

    @property
    def pub_key(self):
        return self.public_key
    
    @property
    def priv_key(self):
        return self.private_key
    
    @pub_key.setter
    def pub_key(self, value):
        self.public_key = value
    
    @priv_key.setter
    def priv_key(self, value):
        self.private_key = value
