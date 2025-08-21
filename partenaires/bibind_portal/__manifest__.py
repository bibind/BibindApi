{
    'name': 'Bibind Portal',
    'version': '0.1',
    'summary': 'Customer portal for managing services',
    'author': 'Bibind',
    'depends': ['portal', 'web', 'mail', 'bus', 'bibind_core'],
    'data': [
        'data/res_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/portal_menu.xml',
    ],
    'application': False,
    'installable': True,
}
