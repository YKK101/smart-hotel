#!/bin/sh
set -e

db_hostname="$1"
db_port="$2"
db_username="$3"
db_password="$4"
dn_name="$5"
db_server_name="$6"
debezium_hostname="$7"
debezium_port="$8"

# Register sink connector for TimescaleDB (destination)
echo "Registering TimescaleDB sink connector..."
curl -X POST -H "Content-Type: application/json" \
    --data "{
      \"name\": \"central-postgres-sink\",
      \"config\": {
        \"connector.class\": \"io.debezium.connector.jdbc.JdbcSinkConnector\",
        \"tasks.max\": \"1\",
        \"connection.url\": \"jdbc:postgresql://$db_hostname:$db_post/$db_name\",
        \"connection.username\": \"$db_username\",
        \"connection.password\": \"$db_password\",
        \"auto.create\": \"true\",
        \"auto.evolve\": \"true\",
        \"schema.evolution\": \"basic\",
        \"database.time_zone\": \"UTC\",
        \"insert.mode\": \"upsert\",
        \"table.name.format\": \"${topic}\",
        \"topics.regex\": \"smarthotel\\.public\\..*\",
        \"primary.key.mode\": \"record_value\",
        \"primary.key.fields\": \"id\"
      }
    }" http://$debezium_hostname:$debezium_port/connectors

echo "Connectors registered successfully!"
