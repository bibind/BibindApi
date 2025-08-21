# -*- coding: utf-8 -*-
{
    'name': "Bibind Core",
    'summary': "Core technical module for Bibind ecosystem (OIDC, op_bootstrap client, webhooks, JSON logs)",
    'description': """Bibind Core provides reusable mixins, an HTTP client to op_bootstrap with OIDC client credentials, structured JSON logging, secure webhooks and multi-tenant helpers.""",
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Bibind',
    'website': 'https://example.com',
    'depends': ['base', 'web', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/rules.xml',
        'data/res_groups.xml',
        'data/ir_config_parameter.xml',
        'views/res_config_settings_views.xml',
    ],
    'application': False,
}
