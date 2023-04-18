# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Original Copyright 2015 Eezee-It, modified and maintained by Odoo.

import logging

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request
from werkzeug.urls import url_join, url_encode

_logger = logging.getLogger(__name__)


class PointPayment(http.Controller):

    @http.route('/shpping/point/payment', type='http', auth='public', methods=['post'], website=True)
    def point_payment_methods(self, **post):
        partner = request.env.user.partner_id

        shipping_id = post['order_id']
        shipping_order = request.env['shipping.bill'].browse(int(shipping_id))

        point_balance = partner.wallet_balance
        shipping_invoice = shipping_order.sale_invoice_ids.filtered(lambda l: l.payment_state not in ['paid', 'reversed', 'invoicing_legacy'])
        shipping_sale = shipping_order.sale_order_id

        if point_balance > sum(shipping_invoice.mapped('amount_total')):
            wallet_id = request.env['website.wallet.transaction'].create({
                'wallet_type': 'debit',
                'partner_id': partner.id,
                'sale_order_id': shipping_sale.id,
                'reference': 'sale_order',
                'amount': sum(shipping_invoice.mapped('amount_total')),
                'currency_id': shipping_order.currency_id.id,
                'status': 'done'
            })

            shipping_sale.write({
                'wallet_used': shipping_sale.amount_total,
                'wallet_transaction_id': wallet_id.id
            })

            for invoice in shipping_invoice:
                invoice.state = 'draft'
                val = {
                    'name': 'Wallet Used' + ' ' + str(invoice.amount_total),
                    'quantity': 1,
                    'price_unit': -invoice.amount_total
                }
                invoice.update({
                    'invoice_line_ids': [(0, 0, val)]
                })

                # invoice.action_post()
                invoice.state = 'posted'

        return request.redirect('/sale/portal/orders?ytype=valued')



