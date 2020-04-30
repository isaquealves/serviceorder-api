from app.providers.schema import ma
from flask_marshmallow.fields import fields
from .validators import username_is_valid


class UserSchema(ma.Schema):
    """
    User serialization/deserialization schema
    """
    class Meta:
        ordered = True

    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=username_is_valid)
    public_key = fields.Str(dump_only=True)
