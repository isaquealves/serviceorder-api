from app.providers.schema import ma
from flask_marshmallow.fields import fields
from marshmallow import validates_schema, ValidationError
from .validators import username_is_valid


class UserSchema(ma.Schema):
    """
    User serialization/deserialization schema
    """

    class Meta:
        ordered = True

    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    email = fields.Email(required=False)
    username = fields.Str(required=False, validate=username_is_valid)
    public_key = fields.Str(dump_only=True)

    @validates_schema
    def check_for_username_or_email(self, data, **kwargs):
        if not any(lambda x: x in data.keys() for x in ["username", "email"]):
            raise ValidationError(
                'At least one of "email" or "username" should be informed'
            )
