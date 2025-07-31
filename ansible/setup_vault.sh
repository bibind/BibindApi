#!/bin/bash
# Script to prepare Vault for op_bootstrap
set -euo pipefail

# Enable KV secrets engine at path bibind if not already
vault secrets enable -path=bibind kv 2>/dev/null || true

# Create policy allowing read access to Bibind secrets
cat <<POLICY | vault policy write bibind-op_bootstrap -
path "bibind/data/op_bootstrap/*" {
  capabilities = ["read", "list"]
}
POLICY

# Example secret placeholder
vault kv put bibind/op_bootstrap/example placeholder=value
