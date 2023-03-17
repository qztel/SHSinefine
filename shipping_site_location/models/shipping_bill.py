# import logging

from odoo import models, fields, api, _


# from odoo.exceptions import UserError
# _logger = logging.getLogger(__name__)


class ShippingBill(models.Model):
    _inherit = 'shipping.bill'

    # 仓库位置
    site_location_id = fields.Many2one('site.location', string="仓库位置")

    def _inverse_frontend_trigger(selfs):
        for self in selfs.filtered(lambda s:s.frontend_trigger):
            getattr(self, self.frontend_trigger)()
            self.write({'frontend_trigger': False})

    frontend_trigger = fields.Char(inverse='_inverse_frontend_trigger')

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            sale_order = self.env['sale.order'].search(
                [('shipping_no', 'ilike', self.name), ('shipping_bill_id', '=', False)], limit=1)
            if sale_order:
                self.update({
                    'sale_order_id': sale_order.id,
                    'no_change': sale_order.no_change,
                    'frontend_trigger': 'multi_action_match',
                })
            else:
                self.update({
                    'sale_order_id': False,
                    'no_change': False,
                    'frontend_trigger': 'multi_action_match',
                    'site_location_id': 1
                })

    @api.onchange('shipping_factor_id', 'sale_site_id')
    def onchange_site_location(selfs):
        for self in selfs:
            if self.shipping_factor_id and self.sale_site_id:
                site_location_id = self.env['site.location'].search([
                    ('factor_id', '=', self.shipping_factor_id.id),
                    ('site_partner_id', '=', self.sale_site_id.id)
                ])
                if site_location_id:
                    self.site_location_id = site_location_id.id


