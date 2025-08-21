from unittest import mock

import pytest

from odoo.tests.common import TransactionCase


class ApiClientCase(TransactionCase):
    def setUp(self):  # noqa:D401
        super().setUp()
        self.client = self.env["bibind.api_client"]

    @mock.patch("requests.post")
    @mock.patch("requests.Session.request")
    def test_get_context(self, m_req, m_post):
        m_post.return_value.status_code = 200
        m_post.return_value.json.return_value = {
            "access_token": "t", "expires_in": 60
        }
        m_req.return_value.status_code = 200
        m_req.return_value.json.return_value = {"pong": True}
        data = self.client.get_context("ping")
        assert data["pong"] is True
        assert m_req.call_args[1]["headers"]["Authorization"].startswith("Bearer ")
