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

    @mock.patch("requests.post")
    @mock.patch("requests.Session.request")
    def test_refresh_token_on_401(self, m_req, m_post):
        token1 = mock.Mock()
        token1.status_code = 200
        token1.json.return_value = {"access_token": "t1", "expires_in": 60}
        token2 = mock.Mock()
        token2.status_code = 200
        token2.json.return_value = {"access_token": "t2", "expires_in": 60}
        m_post.side_effect = [token1, token2]
        resp_401 = mock.Mock()
        resp_401.status_code = 401
        resp_ok = mock.Mock()
        resp_ok.status_code = 200
        resp_ok.json.return_value = {"pong": True}
        m_req.side_effect = [resp_401, resp_ok]
        data = self.client.get_context("ping")
        assert data["pong"] is True
        assert m_post.call_count == 2
        # second request should use refreshed token
        auth_header = m_req.call_args_list[-1][1]["headers"]["Authorization"]
        assert auth_header == "Bearer t2"

    @mock.patch("requests.post")
    @mock.patch("requests.adapters.HTTPAdapter.send")
    def test_retries_on_errors(self, m_send, m_post):
        m_post.return_value.status_code = 200
        m_post.return_value.json.return_value = {"access_token": "t", "expires_in": 60}
        bad = mock.Mock()
        bad.status_code = 500
        bad.read = lambda *a, **k: b""  # needed by requests
        good = mock.Mock()
        good.status_code = 200
        good.read = lambda *a, **k: b"{}"
        good.json.return_value = {"pong": True}
        m_send.side_effect = [bad, good]
        data = self.client.get_context("ping")
        assert data["pong"] is True
        assert m_send.call_count == 2

    @mock.patch("requests.post")
    @mock.patch("requests.Session.request")
    def test_circuit_breaker_open(self, m_req, m_post):
        from odoo.addons.bibind_core.models.api_client import _CircuitBreaker, ApiClientServerError, ApiClientCircuitOpen

        m_post.return_value.status_code = 200
        m_post.return_value.json.return_value = {"access_token": "t", "expires_in": 60}
        resp = mock.Mock()
        resp.status_code = 500
        m_req.return_value = resp
        self.client._breaker = _CircuitBreaker(fail_max=1, reset_timeout_s=60)
        with pytest.raises(ApiClientServerError):
            self.client.get_context("ping")
        with pytest.raises(ApiClientCircuitOpen):
            self.client.get_context("ping")
        # second call should not reach request due to open circuit
        assert m_req.call_count == 1
