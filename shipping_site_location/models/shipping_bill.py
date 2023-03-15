# import logging

from odoo import models, fields, api, _
# from odoo.exceptions import UserError
# _logger = logging.getLogger(__name__)


class ShippingBill(models.Model):
    _inherit = 'shipping.bill'

    # 仓库位置
    site_location_id = fields.Many2one('site.location', string="仓库位置")

