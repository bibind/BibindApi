#!/bin/bash
# Simple helper to create Kafka topics defined in so_mapping.yaml

MAPPING_FILE="$(dirname "$0")/../Bibind/op_bootstrap/app/config/so_mapping.yaml"
BOOTSTRAP_SERVERS=${BOOTSTRAP_SERVERS:-localhost:9092}

if ! command -v kafka-topics >/dev/null 2>&1; then
  echo "kafka-topics command not found" >&2
  exit 1
fi

TOPICS=$(python - <<PY
import yaml,sys
with open('$MAPPING_FILE') as f:
    data=yaml.safe_load(f)
for t in data['topics'].values():
    print(t)
PY
)

for topic in $TOPICS; do
  kafka-topics --bootstrap-server "$BOOTSTRAP_SERVERS" --create --if-not-exists --topic "$topic"
done
