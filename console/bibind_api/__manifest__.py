{
    "name": "Bibind API",
    "version": "1.0",
    "summary": "Module permettant de consommer l'API Bibind",
    "author": "Bibind",
    "license": "AGPL-3",
    "depends": [
        "base",
        "hr",
        "hr_recruitment",
        "website_hr_recruitment",
        "product",
        "account",
        "project",
        "elearning",
        "website"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/templates.xml",
        "data/elearning_courses.xml",
        "default_configuration.xml",
        "job_positions_data.xml",
        "'department_data.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True
}