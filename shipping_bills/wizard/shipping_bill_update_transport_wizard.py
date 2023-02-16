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
            shipping_bill = self.env['shipping.bill'].search([
                '|', ('name', '=', _name), ('sale_fetch_no', '=', _name),
                ('state', '=', 'valued')], limit=1)
            shipping_bills |= shipping_bill

            shipping_bill.write({
                'out_date': _today,
                'logistics': logistics,
                'tracking_no': tracking_no,
                'state': 'transported',
            })
            # 获取大包裹分组
            group_dict = {
                'logistics': logistics,
                'tracking_no': tracking_no,
                'site_id': shipping_bill.sale_site_id.id
            }
            if group_dict not in groupby_arr:
                groupby_arr.append(group_dict)

        if not shipping_bills:
            raise UserError('不存在对应的包裹。')

        # 创建大包裹
        for line in groupby_arr:
            large_parcel = self.env['shipping.large.parcel'].create({
                'name': self.env['ir.sequence'].next_by_code('shipping.large.parcel'),
                'site_id': line['site_id'],
                'logistics_provider': line['logistics'],
                'logistics_tracking_code': line['tracking_no']
            })
            shipping_bills.filtered(lambda l: l.logistics == line['logistics'] and l.tracking_no == line['tracking_no'])['large_parcel'] = large_parcel.id

            # 发送邮件
            template = self.env.ref('shipping_bills.mail_template_shipping_large_parcel')
            email = template.send_mail(large_parcel.id, raise_exception=True)
            email_email = self.env['mail.mail'].browse(email)
            email_email.send()


