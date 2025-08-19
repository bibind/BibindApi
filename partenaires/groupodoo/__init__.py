try:
    from . import models  # noqa: F401
    from . import controllers  # noqa: F401
except Exception:  # pragma: no cover - allows running tests without odoo
    pass
