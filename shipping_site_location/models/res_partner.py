# import logging

from odoo import models, fields, api, _
# from odoo.exceptions import UserError
# _logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # 仓库位置
    site_location_ids = fields.Many2many('site.location', string="仓库位置")

