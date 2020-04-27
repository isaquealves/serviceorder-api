from app.providers.schema import ma
from flask_marshmallow.fields import fields
from .validators import username_is_valid


class UserSchema(ma.Schema):
    username =  fields.Str(validate=username_is_valid)
    public_key = fields.Str(dump_only=True)
    private_key = fields.Str(dump_only=True)
