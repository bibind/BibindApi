import pytest

from odoo import fields, models
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase

from odoo.addons.bibind_core.models.mixins import PceMixin


class Dummy(models.Model, PceMixin):
    _name = "bibind.test.pce"
    name = fields.Char()


class DummyModelCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # register dummy model
        cls.env.registry.models[Dummy._name] = Dummy
        Dummy._build_model(cls.env.registry, cls.env.cr)
        cls.env["ir.model"].create({"name": "Dummy", "model": Dummy._name})
        cls.Dummy = cls.env[Dummy._name]
        setattr(cls.env.user, "tenant_id", "t1")

    def test_cross_tenant_access_error(self):
        helpers = self.env["bibind.security.helpers"]
        rec1 = self.Dummy.create({"name": "A", "tenant_id": "t1"})
        helpers.check_tenant(rec1)  # should pass
        rec2 = self.Dummy.create({"name": "B", "tenant_id": "t2"})
        with pytest.raises(AccessError):
            helpers.check_tenant(rec2)
