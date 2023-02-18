# See LICENSE file for full copyright and licensing details.
import odoo
from odoo import fields, models, api
from odoo.exceptions import UserError

class ShippingBill(models.Model):
    _inherit = 'shipping.bill'

    @api.depends('sale_order_id.order_line')
    def _compute_sale_order_line_ids(selfs):
        for self in selfs:
            self.sale_order_line_ids = self.sale_order_id.order_line
    sale_order_line_ids = fields.Many2many('sale.order.line',compute='_compute_sale_order_line_ids')


