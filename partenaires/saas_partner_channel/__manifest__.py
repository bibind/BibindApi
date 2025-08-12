# -*- coding: utf-8 -*-
{
    'name': 'SaaS Partner Channel',
    'version': '17.0.1.0.0',
    'summary': 'Programme revendeur pour plateforme SaaS',
    'category': 'Sales/CRM',
    'author': 'OpenAI',
    'website': 'https://example.com',
    'depends': [
        'base', 'contacts', 'mail', 'crm', 'sale', 'sale_subscription',
        'account', 'payment', 'website', 'portal', 'helpdesk', 'sign', 'documents'
    ],
    'data': [
        'security/rules.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/portal_menus.xml',
        'data/mail_templates.xml',
        'data/demo.xml',
        'views/partner_views.xml',
        'views/tenant_views.xml',
        'views/deal_views.xml',
        'views/commission_views.xml',
        'views/payout_views.xml',
        'views/wizard_views.xml',
        'views/portal_templates.xml',
        'report/payout_self_billing.xml',
    ],
    'demo': [],
    'installable': True,
    'license': 'LGPL-3',
}
