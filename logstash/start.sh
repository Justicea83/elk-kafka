#!/bin/bash

# Variables
TEMPLATE_PATH="/logstash_dir/nyc_311_service_requests_template.json"
ELASTICSEARCH_ENDPOINT="http://elasticsearch:9200"
TEMPLATE_NAME="nyc_311_service_requests_template"

# Wait for Elasticsearch to be available
echo "Waiting for Elasticsearch to be available..."
until $(curl --output /dev/null --silent --head --fail "$ELASTICSEARCH_ENDPOINT"); do
  printf '.'
  sleep 5
done
echo "Elasticsearch is available."

# Applying the template
echo "Applying index template..."
curl -X PUT "${ELASTICSEARCH_ENDPOINT}/_index_template/${TEMPLATE_NAME}" \
  -H 'Content-Type: application/json' \
  -d "@${TEMPLATE_PATH}"

echo "Index template applied successfully."
