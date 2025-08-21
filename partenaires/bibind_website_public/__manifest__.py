# -*- coding: utf-8 -*-
"""Manifest for Bibind Website Public addon."""
{
    'name': 'bibind_website_public',
    'version': '1.0',
    'summary': 'Public website for Bibind',
    'category': 'Website',
    'depends': ['website', 'bibind_core'],
    'data': [
        'data/website_menu.xml',
        'data/mail_templates.xml',
        'views/website_pages.xml',
        'views/website_seo_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bibind_website_public/static/src/css/theme.css',
            'bibind_website_public/static/src/js/ui.js',
        ],
    },
    'license': 'LGPL-3',
}
