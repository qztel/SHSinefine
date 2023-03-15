# import logging

from odoo import models, fields, api, _


# from odoo.exceptions import UserError
# _logger = logging.getLogger(__name__)


class SiteLocation(models.Model):
    _name = 'site.location'

    name = fields.Char('位置')
    factor_id = fields.Many2one('shipping.factor', '敏感性')
    shipping_bill_id = fields.Many2one('shipping.bill', '运单')
