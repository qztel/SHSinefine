# -*- coding: utf-8 -*-
{
    'name': "OSCG-POS-Report",
    'description': """
        OSCG-POS-Report
    """,

    'author': "OSCG-Wang",
    'website': "http://www.oscg.cn",
    'category': 'project',
    'version': '0.1',
    'depends': [
        'base', 'point_of_sale'
        ],
    'data': [

    ],
    'assets': {
        'web.assets_qweb': [
            'oscg_pos_report_xml/static/src/xml/oscg_pos_report_xml.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
