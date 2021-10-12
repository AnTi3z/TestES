#!/bin/bash
host=${ELASTICSEARCH_URL="http://localhost:9200"}

function elastic_ready {
  health="$(curl -fsSL "$host/_cat/health?h=status")"
  if [ "$health" = "yellow" ]; then
    return 0
  fi
  return 1
}

until elastic_ready; do
  echo "Waiting for Elasticsearch service up..."
  sleep 5
done
echo "Elasticsearch service ready!"

venv/bin/python db_init.py
venv/bin/python main.py
