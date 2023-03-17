from odoo import models, fields, api, _


class ShippingState(models.Model):
    _name = 'shipping.state'
    _description = '阶段'

    name = fields.Char('名称')
    fold = fields.Boolean('是否在看板中折叠？')

