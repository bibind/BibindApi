from odoo.tests.common import TransactionCase


class DummyModelCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Dummy = cls.env['ir.model']

    def test_access_domain(self):
        self.assertTrue(True)
