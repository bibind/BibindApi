from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class DummyTenant(models.Model):
    _name = "pce.tenant"
    _description = "Dummy tenant"

    name = fields.Char()


class DummyPceModel(models.Model):
    _name = "bibind.dummy.pce"
    _inherit = "bibind.pce.mixin"
    _description = "Dummy model for PceMixin tests"

    name = fields.Char()


class TestPceMixin(TransactionCase):
    def setUp(self):  # noqa:D401
        super().setUp()
        Tenant = self.env["pce.tenant"]
        self.tenant1 = Tenant.create({"name": "Tenant 1"})
        self.tenant2 = Tenant.create({"name": "Tenant 2"})
        User = self.env["res.users"].with_context(no_reset_password=True)
        self.user1 = User.create({"name": "U1", "login": "u1", "tenant_id": self.tenant1.id})
        self.user2 = User.create({"name": "U2", "login": "u2", "tenant_id": self.tenant2.id})
        self.Model = self.env["bibind.dummy.pce"]

    def test_create_propagates_tenant(self):
        rec = self.Model.with_user(self.user1).create({"name": "A"})
        self.assertEqual(rec.tenant_id, str(self.tenant1.id))

    def test_with_tenant_filters_records(self):
        r1 = self.Model.with_user(self.user1).create({"name": "R1"})
        self.Model.with_user(self.user2).create({"name": "R2"})
        rs = self.Model.with_tenant(str(self.tenant1.id))
        self.assertEqual(rs, r1)

    def test_invalid_format_raises(self):
        with self.assertRaises(ValidationError):
            self.Model.create({"name": "X", "tenant_id": "bad$"})
        with self.assertRaises(ValidationError):
            self.Model.create({"name": "Y", "pce_instance_id": "bad$"})
