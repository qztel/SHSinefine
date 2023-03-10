# See LICENSE file for full copyright and licensing details.
import odoo
from odoo import fields, models, api
from odoo.exceptions import UserError

class ProductCategoryDetermined(models.Model):
    _name = 'product.category.determined'

    name = fields.Char('名称')


