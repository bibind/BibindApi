# Bibind Core

Base module providing common services for Bibind ecosystem.

## Features
- Reusable mixins for audit, tenant isolation and JSON logging
- HTTP client to `op_bootstrap` with OIDC client-credentials and resiliency
- Secure webhook endpoints for audit events and AI callbacks
- Configuration panel under *Settings → Technical → Bibind Core*

## Configuration Parameters
| Key | Description |
| --- | --- |
| `op_bootstrap_base_url` | Base URL of op_bootstrap |
| `kc_token_url` | Keycloak token endpoint |
| `kc_client_id_ref` | Vault reference for client id |
| `kc_client_secret_ref` | Vault reference for client secret |
| `http_timeout_s` | HTTP timeout in seconds |
| `http_retry_total` | Number of retries |
| `http_backoff_factor` | Backoff factor |
| `breaker_fail_max` | Maximum failures before opening circuit |
| `breaker_reset_s` | Circuit reset timeout |
| `log_level` | Logging level |

Secrets must be stored in Vault and referenced using `vault:` URIs.

## Usage
Example of calling the client from another module:
```python
client = self.env['bibind.api_client']
ctx = client.get_context('instance-id')
```

## Tests
Run tests with:
```bash
pytest partenaires/bibind_core/tests -q
```

## Compatibility
- Odoo 18

## Limitations
- Circuit breaker is in-memory per worker
```
