#!/bin/sh
set -e

connector_name="$1"
db_hostname="$2"
db_port="$3"
db_username="$4"
db_password="$5"
dn_name="$6"
db_server_name="$7"
debezium_hostname="$8"
debezium_port="$9"

# Register source connector for TimescaleDB (source)
echo "Registering TimescaleDB source connector..."
curl -X POST -H "Content-Type: application/json" \
    --data "{
      \"name\": \"$connector_name-source\",
      \"config\": {
        \"connector.class\": \"io.debezium.connector.postgresql.PostgresConnector\",
        \"tasks.max\": \"1\",
        \"plugin.name\": \"pgoutput\",
        \"database.hostname\": \"$db_hostname\",
        \"database.port\": \"$db_port\",
        \"database.user\": \"$db_username\",
        \"database.password\": \"$db_password\",
        \"database.dbname\": \"$db_name\",
        \"database.server.name\": \"$db_servername\",
        \"table.include.list\": \"public.*\",
        \"schema.include.list\": \"public\",
        \"topic.prefix\": \"smarthotel\",
      }
    }" http://$debezium_hostname:$debezium_port/connectors

echo "Connectors registered successfully!"
