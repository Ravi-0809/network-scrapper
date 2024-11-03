from marshmallow import Schema, fields

class URLInput(Schema):
    url = fields.Str(required=True)
    username = fields.Str(allow_none=True)
    password = fields.Str(allow_none=True)

class URLInputRead(Schema):
    url = fields.Str(required=True)