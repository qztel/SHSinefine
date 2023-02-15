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

        site = False
        logistics_provider = False
        logistics_tracking_code = False
        parcel_exists = False

        # 创建大包裹
        large_parcel = self.env['shipping.large.parcel'].create({
            'name': self.env['ir.sequence'].next_by_code('shipping.large.parcel'),
        })

        dispatch_time = large_parcel.create_date.strftime('%Y年%m月%d日 %H:%M:%S')
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
            if shipping_bill and not parcel_exists:
                parcel_exists = True
            if not site:
                site = shipping_bill.sale_site_id.id
            if not logistics_provider or not logistics_tracking_code:
                logistics_provider = logistics
                logistics_tracking_code = tracking_no

            shipping_bill.write({
                'out_date': _today,
                'logistics': logistics,
                'tracking_no': tracking_no,
                'state': 'transported',
                'large_parcel': large_parcel.id
            })

        if not parcel_exists:
            raise UserError('不存在对应的包裹。')

        large_parcel.write({
            'site_id': site,
            'logistics_provider': logistics_provider,
            'logistics_tracking_code': logistics_tracking_code
        })

        # 发送邮件
        template = self.env.ref('shipping_bills.mail_template_guidelines', raise_if_not_found=False)
        email = template.sudo().send_mail(large_parcel.id, raise_exception=True)
        email_email = self.env['mail.mail'].sudo().browse(email)
        email_email.sudo().send()


