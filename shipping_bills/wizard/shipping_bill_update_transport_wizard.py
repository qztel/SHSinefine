# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, datetime


class ShippingBillUpdateTransportWizard(models.TransientModel):
    _name = 'shipping.bill.update.transport.wizard'

    data = fields.Text('数据')

    def apply(self):
        _today = date.today()

        groupby_arr = []
        shipping_bills = self.env['shipping.bill']
        for i, data in enumerate(self.data.split('\n')):
            if not data:
                continue
            _datas = data.split('\t')
            if len(_datas) != 3:
                raise UserError(f'第{i+1}次 数据异常')
            _name, logistics, tracking_no = _datas
            _name, logistics, tracking_no = _name.strip(), logistics.strip(), tracking_no.strip()
            # shipping_bill = self.env['shipping.bill'].search([
            #     '|', ('name', '=', _name), ('sale_fetch_no', '=', _name),
            #     ('state', '=', 'valued')], limit=1)
            shipping_bill = self.env['shipping.bill'].search([('name', '=', _name)])

            shipping_bills |= shipping_bill

            shipping_bill.write({
                'out_date': _today,
                'logistics': logistics,
                'tracking_no': tracking_no,
                'state': 'transported',
            })
        if not shipping_bills:
            raise UserError('不存在对应的包裹。')

        # 创建大包裹

        # 获取大包裹分组
        for term in shipping_bills.mapped(lambda s: (s.logistics, s.tracking_no, s.sale_site_id.id)):
            this_shipping_bills = shipping_bills.filtered(lambda s: (s.logistics, s.tracking_no, s.sale_site_id.id) == term)

            if not this_shipping_bills:
                continue

            large_parcel = self.env['shipping.large.parcel'].create({
                'name': self.env['ir.sequence'].next_by_code('shipping.large.parcel'),
                'site_id': term[2],
                'logistics_provider': term[0],
                'logistics_tracking_code': term[1],
                'shipping_bill_ids': [(6, 0, this_shipping_bills.ids)]
            })
            large_parcel.resend_email()

