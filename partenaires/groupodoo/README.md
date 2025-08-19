# Groupodoo Chat Module

This module adds simple chat widgets connected to the Bibind API. It defines
basic models for chat sessions and messages, a minimal controller for sending
messages and receiving webhook callbacks, and frontend assets for displaying the
chat in Odoo.

## Installation

Add this module to your Odoo addons path and update the app list. Enable the
`Groupodoo` application and configure the API keys in *Settings > General
Settings*.

## Endpoints

- `/groupodoo/api/chat/send` – send a message for a session.
- `/groupodoo/api/chat/webhook` – receive messages from Bibind (signed via
  `X-Bibind-Signature`).

## Testing

Run the Python tests with:

```bash
pytest partenaires/groupodoo/tests -q
```
