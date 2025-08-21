{
    "name": "Bibind Portal",
    "version": "0.1",
    "summary": "Customer portal for managing services",
    "author": "Bibind",
    "depends": ["portal", "web", "mail", "bus", "bibind_core"],
    "data": [
        "security/ir.model.access.csv",
        "security/rules.xml",
        "views/portal_menu.xml",
        "views/wizards.xml",
    ],
    "application": False,
    "installable": True,
}
