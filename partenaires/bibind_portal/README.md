# Bibind Portal

Minimal customer portal for Bibind services.  This addon exposes customer
facing pages under `/my` allowing users to list their services and access
monitoring links.  It demonstrates tenant isolation and basic integration with
`bibind_core` API client.

## Installation

1. Add `bibind_portal` to your Odoo addons path.
2. Update the app list and install *Bibind Portal*.

## Tests

Run unit tests with:

```bash
pytest partenaires/bibind_portal/tests
```
