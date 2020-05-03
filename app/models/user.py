from typing import AnyStr
from orator import SoftDeletes
from app.providers.database import db


class User(SoftDeletes, db.Model):

    public_key: AnyStr
    private_key: AnyStr

    __table__ = 'users'

    __fillable__ = ['first_name', 'last_name', 'email', 'username', 'active']
    __primary_key__ = 'id'
    __guarded__ = ['id', 'public_key', 'private_key']
    __dates__ = ['deleted_at']

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
