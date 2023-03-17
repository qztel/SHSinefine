{
    'name': 'shipping_site_location',
    'description': 'Shipping Bills Site Location',
    'category': 'Operations/Inventory',
    'summary': 'Shipping Bills Site Location',
    'sequence': 300,
    'version': '15.1.0',
    'website': 'http://www.oscg.cn/',
    'author': 'OSCG',
    'license': 'AGPL-3',
    'depends': ['base', 'shipping_bills',],
    'data': [
        'security/ir.model.access.csv',
        'views/site_location.xml',
        'views/res_partner.xml',
        'views/shipping_bill.xml',
        'views/shipping_bill_scan_code.xml',
        'views/action.xml',
        'views/menu.xml',
        'data/site_location.xml',
        'data/ir_actions_server.xml',
    ],

}
