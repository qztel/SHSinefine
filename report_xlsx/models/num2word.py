# -*- coding: utf-8 -*-
# 转换数字到中文大写格式 參考：https://www.jianshu.com/p/a55ac7f148ee
from odoo import fields, models


class AccountInvoice(models.AbstractModel):
    _inherit = "base"

    # 第二个转换函数
    def IIf(self, b, s1, s2):
        if b:
            return s1
        else:
            return s2

    def num2chn(self, nin=None):
        cs = (
        '零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '◇', '分', '角', '元', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿',
        '拾', '佰', '仟', '万')
        st = ''
        st1 = ''
        s = '%0.2f' % nin
        sln = len(s)
        if sln > 15:
            return None
        fg = (nin < 1)
        for i in range(0, sln - 3):
            ns = ord(s[sln - i - 4]) - ord('0')
            st = self.IIf((ns == 0) and (fg or (i == 8) or (i == 4) or (i == 0)), '', cs[ns]) + self.IIf(
                (ns == 0) and ((i != 8) and (i != 4) and (i != 0) or fg and (i == 0)), '', cs[i + 13]) + st
            fg = (ns == 0)
        fg = False
        for i in [1, 2]:
            ns = ord(s[sln - i]) - ord('0')
            st1 = self.IIf((ns == 0) and ((i == 1) or (i == 2) and (fg or (nin < 1))), '', cs[ns]) + self.IIf((ns > 0),
                                                                                                              cs[
                                                                                                                  i + 10],
                                                                                                              self.IIf((
                                                                                                                                   i == 2) or fg,
                                                                                                                       '',
                                                                                                                       '整')) + st1
            fg = (ns == 0)
        st.replace('亿万', '万')
        return self.IIf(nin == 0, '零', st + st1)
