{
  "name": "Group Odoo Chat (Bibind/n8n)",
  "version": "18.0.1.0.0",
  "summary": "Widgets de chat connectés à Bibind (op_bootstrap) pour lancer des workflows n8n avec agents IA",
  "author": "Bibind",
  "category": "Productivity",
  "depends": ["base", "web", "bus", "mail"],
  "data": [
    "security/ir.model.access.csv",
    "security/groupodoo_security.xml",
    "views/chat_session_views.xml",
    "views/res_config_settings_views.xml",
    "data/params.xml",
  ],
  "assets": {
    "web.assets_backend": [
      "groupodoo/static/src/js/chat_widget.js",
      "groupodoo/static/src/xml/chat_widget.xml",
      "groupodoo/static/src/scss/chat.scss",
    ],
    "web.assets_frontend": [
      "groupodoo/static/src/js/chat_widget.js",
      "groupodoo/static/src/xml/chat_widget.xml",
      "groupodoo/static/src/scss/chat.scss",
    ],
  },
  "application": True,
  "license": "LGPL-3",
}
