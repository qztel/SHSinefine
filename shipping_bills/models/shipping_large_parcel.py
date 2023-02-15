# See LICENSE file for full copyright and licensing details.
import odoo
from odoo import fields, models, api
from odoo.exceptions import UserError

class ShippingLargeParcel(models.Model):
    _name = 'shipping.large.parcel'
    _description = "大包裹"
    _rec_name = 'name'

    name = fields.Char('包裹号')
    logistics_provider = fields.Char('物流商', readonly=True)
    logistics_tracking_code = fields.Char('物流追踪码', readonly=True)
    customer_waybill_ids = fields.One2many('shipping.bill', 'large_parcel', string='客户运单', readonly=True)
    site_id = fields.Many2one('res.partner', '站点')




