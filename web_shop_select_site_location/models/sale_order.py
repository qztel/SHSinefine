# import logging

from odoo import models, fields, api, _


# from odoo.exceptions import UserError
# _logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pending_sites = fields.Many2one('res.partner', string='待定站点')