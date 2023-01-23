from marshmallow import Schema, fields

class udsMetaSchema(Schema):
    uniq_id = fields.String()
    stor_folder = fields.String()
    obj_assoc_inv_nums = fields.String()
    obj_authors = fields.String()
    obj_name = fields.String()


class OrderSchema(Schema):
    datetimeAppend = fields.DateTime()
    status = fields.Boolean()
    uds = fields.Nested(udsMetaSchema)

