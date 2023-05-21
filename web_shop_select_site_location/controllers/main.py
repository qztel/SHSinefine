# -*- coding: utf-8 -*-
import datetime
import requests
import logging
import json
from datetime import datetime

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
odoo_session = requests.Session()


class WenShopSelectSiteLocation(http.Controller):

    @http.route(['/select/delivery/type'], type='http', auth="user", website=True)
    def website_select_delivery_type(self, **post):
        order = request.website.sale_get_order()
        if post.get('site_id') != '':
            site_partner = request.env['crm.team'].browse(int(post.get('site_id'))).site_id.id
        else:
            site_partner = order.partner_id.team_id.site_id
        order.sudo().write({
            'carrier_id': int(post.get('type_id')),
            'partner_team_site_id':site_partner
        })
        return {'state': '200'}
